"""One immutable monthly union pass plus bounded original macro/event source intake."""
import json
import re
import xml.etree.ElementTree as ET
from zipfile import ZipFile
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
from .core import *


def utc_timestamps(values):
    """Accept documented UTC datetimes or explicit epoch units, never a local naive offset."""
    if pd.api.types.is_integer_dtype(values):
        middle=float(np.median(values));unit='ns' if middle>1e17 else 'us' if middle>1e14 else 'ms' if middle>1e11 else 's'
        return pd.to_datetime(values,unit=unit,utc=True)
    return pd.to_datetime(values,utc=True)


def reconcile(frame):
    """Collapse exact duplicate observations; exclude every conflicting key, retain counts."""
    key=['ticker','timestamp'];cols=['open','high','low','close','volume']
    frame=frame.drop_duplicates(key+cols).copy();conflict=frame.duplicated(key,keep=False)
    count=int(conflict.sum());frame=frame.loc[~conflict].copy()
    numeric=frame[cols].to_numpy(float)
    valid=np.isfinite(numeric).all(axis=1)&(numeric[:,:4]>0).all(axis=1)&(numeric[:,4]>=0)
    valid&=(frame.high>=frame[['open','close','low']].max(axis=1))&(frame.low<=frame[['open','close','high']].min(axis=1))
    frame['is_valid']=valid;frame['is_genuine']=True;frame['is_imputed']=False
    return frame.sort_values(key).reset_index(drop=True),dict(conflicting_rows_excluded=count,invalid_rows_retained_flagged=int((~valid).sum()))


def extract_month(raw,month,symbols,output):
    """Bounded row-batch decode; retain only frozen missing symbols and RTH minute rows."""
    chunks=[];read=0;pf=pq.ParquetFile(raw)
    required=['timestamp','ticker','open','high','low','close','volume']
    if not set(required)<=set(pf.schema_arrow.names):raise ValueError('HF_SCHEMA_MISMATCH: '+str(pf.schema_arrow))
    for batch in pf.iter_batches(batch_size=65536,columns=required):
        read+=len(batch);mask=pc.is_in(batch.column('ticker'),value_set=pa.array(symbols))
        selected=batch.filter(mask)
        if len(selected)==0:continue
        f=selected.to_pandas();f['timestamp']=utc_timestamps(f.timestamp)
        et=f.timestamp.dt.tz_convert('America/New_York');minute=et.dt.hour*60+et.dt.minute
        f=f[(minute>=570)&(minute<960)].copy()
        if len(f):chunks.append(f)
    if not chunks:raise ValueError('HF_NO_FROZEN_SYMBOLS: '+month)
    frame=pd.concat(chunks,ignore_index=True)
    if not frame.timestamp.dt.strftime('%Y-%m').eq(month).all():raise ValueError('HF_MONTH_MISMATCH')
    if not (frame.timestamp.dt.second==0).all():raise ValueError('HF_NOT_MINUTE_STARTS')
    frame,qa=reconcile(frame);frame['source_id']='HF_MINUTE_A';frame['source_revision']=HF_REV
    if set(frame.ticker)!=set(symbols):raise ValueError('HF_MISSING_FROZEN_SYMBOL: '+str(set(symbols)-set(frame.ticker)))
    output.parent.mkdir(parents=True,exist_ok=True);tmp=output.with_suffix('.parquet.tmp');frame.to_parquet(tmp,index=False,compression='zstd')
    saved=pq.read_table(tmp);assert len(saved)==len(frame) and not frame.duplicated(['ticker','timestamp']).any()
    tmp.replace(output)
    return dict(rows=len(frame),source_rows_scanned=read,symbol_counts=frame.groupby('ticker').size().to_dict(),**qa,**reference(output))


def read_xlsx(path):
    """Read published workbook values/headers via standard XML; never alter workbook."""
    ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
    with ZipFile(path) as z:
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns):strings.append(''.join(si.itertext()))
        rel=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        targets={e.attrib['Id']:e.attrib['Target'] for e in rel}
        book=ET.fromstring(z.read('xl/workbook.xml'));out={}
        for sheet in book.findall('m:sheets/m:sheet',ns):
            target=targets[sheet.attrib['{'+ns['r']+'}id']];target=target.lstrip('/') if target.startswith('/') else 'xl/'+target
            rows=[]
            for row in ET.fromstring(z.read(target)).findall('m:sheetData/m:row',ns):
                cells={}
                for cell in row.findall('m:c',ns):
                    letters=re.match('[A-Z]+',cell.attrib['r']).group();index=0
                    for c in letters:index=index*26+ord(c)-64
                    v=cell.find('m:v',ns);val=None if v is None else v.text
                    if cell.attrib.get('t')=='s' and val is not None:val=strings[int(val)]
                    elif cell.attrib.get('t')=='inlineStr':val=''.join(cell.find('m:is',ns).itertext())
                    elif val is not None:
                        try:val=float(val)
                        except ValueError:pass
                    cells[index-1]=val
                values=[None]*(max(cells,default=-1)+1)
                for i,v in cells.items():values[i]=v
                rows.append(values)
            out[sheet.attrib['name']]=rows
    return out


def validated_month_output(entry,month,output,revision=HF_REV):
    """A verified checkpoint is sufficient to resume without calling the network."""
    if not entry or entry.get('status')!='validated':return False
    if entry['month']!=month or entry['revision']!=revision:raise ValueError('MONTH_RESUME_SOURCE_CONFLICT')
    if sha(output)!=entry['output']['sha256']:raise ValueError('MONTH_RESUME_HASH_CONFLICT')
    if pq.ParquetFile(output).metadata.num_rows!=entry['output']['rows']:raise ValueError('MONTH_RESUME_COUNT_CONFLICT')
    counts=pq.read_table(output,columns=['ticker']).to_pandas().groupby('ticker').size().to_dict()
    if counts!=entry['output']['symbol_counts']:raise ValueError('MONTH_RESUME_SYMBOL_COUNT_CONFLICT')
    return True


def acquire_all():
    """Only phase allowed to acquire sources; resume never fetches a validated month again."""
    union=json.loads((RUN/'manifests/union_acquisition_plan.json').read_text());registry=json.loads((RUN/'manifests/source_registry.json').read_text())
    for id in IDS:load_config(id)
    if union['dataset']!='mito0o852/OHLCV-1m' or union['revision']!=HF_REV:raise ValueError('SOURCE_ALIAS_FORBIDDEN')
    budget=Budget();ledger=RUN/'checkpoints/hf_months.jsonl';existing={}
    if ledger.exists():
        for line in ledger.read_text().splitlines():
            e=json.loads(line);existing[e['month']]=e
    holds={};outputs=[]
    for m in union['months']:
        month=m['month'];output=DATA/'market_1m'/(month+'.parquet');raw=RUN/'scratch'/(month+'.source.parquet')
        entry=existing.get(month)
        if validated_month_output(entry,month,output):
            outputs.append(entry['output']);print('SKIP_VALIDATED',month,flush=True)
            if raw.exists():
                assert sha(raw)==m['lfs_sha256'];raw.unlink();append_json(RUN/'logs/cleanup.jsonl',dict(path=str(raw.relative_to(ROOT)),reason='validated own raw source; interrupted cleanup recovery',at=now()))
            continue
        budget.check(m['bytes']+100_000_000,'month reservation '+month)
        append_json(ledger,dict(month=month,status='in_progress',revision=HF_REV,at=now(),symbols=union['acquire_symbols']))
        url=f"https://huggingface.co/datasets/{union['dataset']}/resolve/{HF_REV}/{m['path']}"
        print('ACQUIRE',month,m['bytes'],'bytes',flush=True)
        try:
            receipt=download(url,raw,m['bytes'],expected_sha=m['lfs_sha256'],budget=budget)
            budget.check(50_000_000,'filter '+month)
            result=extract_month(raw,month,union['acquire_symbols'],output);outputs.append(result)
            append_json(ledger,dict(month=month,status='validated',revision=HF_REV,at=now(),upstream_sha256=m['lfs_sha256'],etag=receipt['etag'],network_bytes=receipt['bytes'],output=result))
            raw.unlink();append_json(RUN/'logs/cleanup.jsonl',dict(path=str(raw.relative_to(ROOT)),bytes=receipt['bytes'],reason='validated filtered partition, raw never retained across months',at=now()))
            budget.check(0,'month cleaned '+month)
        except Exception as e:
            append_json(ledger,dict(month=month,status='failed',at=now(),reason=type(e).__name__+': '+str(e)[:250]))
            holds['HF_MINUTE_A']=type(e).__name__+': '+str(e)[:250]
            print('SOURCE_HOLD',holds['HF_MINUTE_A'],flush=True);break
    # Independent small-source branches continue if market intake was blocked.
    etf=registry['HF_ETF_DAILY'];small={}
    for name in ['etf_daily_prices.parquet','instrument_metadata.parquet']:
        url=f"https://huggingface.co/datasets/thecharttruth/etf-data/resolve/{etf['revision']}/{name}"
        try:
            p=DATA/'etf_daily'/name;download(url,p,5_000_000,budget=budget);small[name]=reference(p)
        except Exception as e:holds['HF_ETF_DAILY']=type(e).__name__+': '+str(e)[:200]
    for series in ['DGS2','DGS10']:
        url=f'https://fred.stlouisfed.org/graph/?g=1&cosd=2021-04-01&coed=2023-12-29&id={series}'
        # The canonical FRED CSV endpoint, not a chart screenshot or yield-change proxy.
        url=f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}&cosd=2021-04-01&coed=2023-12-29'
        try:
            p=DATA/'fred_rates'/(series+'.csv');download(url,p,1_000_000,budget=budget);small[series]=reference(p)
        except Exception as e:holds['FED_RATES']=type(e).__name__+': '+str(e)[:200]
    try:
        p=DATA/'fed_surprises/monetary-policy-surprises-data.xlsx';download(registry['FED_SHOCKS']['url'],p,3_000_000,budget=budget)
        small['FED_SHOCKS']=reference(p);sheets=read_xlsx(p)
        write_json(RUN/'manifests/fed_workbook_schema.json',{name:dict(rows=len(rows),first_rows=rows[:8]) for name,rows in sheets.items()})
        print('FED_WORKBOOK',[(k,len(v),v[:2]) for k,v in sheets.items()],flush=True)
    except Exception as e:holds['FED_SHOCKS']=type(e).__name__+': '+str(e)[:200]
    chart_links=json.loads((RUN/'manifests/remote_metadata/frbsf_download_links.json').read_text())
    chart_url=next(u for u in chart_links if '.csv' in u.lower())
    try:
        p=DATA/'fed_surprises/published_chart_units_check.csv';download(chart_url,p,1_000_000,budget=budget);small['FED_SHOCKS_CHART_UNITS']=reference(p)
    except Exception as e:holds['FED_SHOCKS_UNITS_CHECK']=str(e)[:180]
    # Official event metadata only, fetched once. Standard release times audited from statements.
    statements={}
    for year in range(2016,2022):
        url=f'https://www.federalreserve.gov/monetarypolicy/fomchistorical{year}.htm';p=DATA/'fed_surprises'/f'calendar_{year}.html'
        try:
            if year==2021:
                # Historical-calendar publication lags five years: direct official
                # statements remain public; use the published FOMC workbook dates.
                rows=read_xlsx(DATA/'fed_surprises/monetary-policy-surprises-data.xlsx')['FOMC (update 2023)']
                dates=sorted({(pd.Timestamp('1899-12-30')+pd.Timedelta(days=row[0])).strftime('%Y%m%d') for row in rows[1:]
                              if isinstance(row[0],(float,int)) and (pd.Timestamp('1899-12-30')+pd.Timedelta(days=row[0])).year==year})
            else:
                download(url,p,2_000_000,budget=budget)
                dates=sorted(set(re.findall(r'pressreleases/monetary(\d{8})a\.htm',p.read_text())))
            for date in dates:
                s=DATA/'fed_surprises'/f'statement_{date}.html';u=f'https://www.federalreserve.gov/newsevents/pressreleases/monetary{date}a.htm'
                try:
                    download(u,s,1_000_000,budget=budget);html=s.read_text();text=re.sub('<[^>]+>',' ',html);text=re.sub(r'\s+',' ',text)
                    match=re.search(r'For release at\s+([0-9:.]+\s*[ap]\.?m\.?(?:\s*[A-Z]{2,4})?)',text,re.I)
                    label=match.group(1) if match else 'NOT_VERIFIED'
                    statements[date]=dict(date_et=date[:4]+'-'+date[4:6]+'-'+date[6:],release_text=label,standard_1400=bool(re.match(r'2[:.]00\s*p',label,re.I)),source=reference(s))
                except Exception as e:statements[date]=dict(date_et=date[:4]+'-'+date[4:6]+'-'+date[6:],release_text='REQUEST_FAILED',standard_1400=False,reason=str(e)[:100])
        except Exception as e:holds['FED_EVENT_CALENDAR_'+str(year)]=str(e)[:180]
    write_json(RUN/'manifests/official_event_times.json',statements)
    write_json(RUN/'manifests/acquired_sources.json',dict(minute_partitions=outputs,small_sources=small,holds=holds,at=now(),source_registry_sha256=sha(RUN/'manifests/source_registry.json')))
    (RUN/'reports/shared_download_integrity.md').write_text('# Shared acquisition integrity\n\n'+json.dumps(dict(months_validated=len(outputs),source_revision=HF_REV,holds=holds,new_minute_symbols=union['acquire_symbols'],reused=['SPY','BAC','KO']),indent=2)+'\n\nRaw monthly temporary files were removed only after selected-output validation; exact bytes/hashes/ETags are in the per-month ledger. No mirror, no dataset snapshot, no package/HF cache used. Small sources are acquired once with immutable receipts. Statement times are primary-source metadata; unverified/non14:00events will be excluded, not shifted.\n')
    budget.check(0,'acquisition complete')
