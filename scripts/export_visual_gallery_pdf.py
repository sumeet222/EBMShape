"""Export the existing Markdown gallery; never recompute scientific results.

Requires reportlab, Pillow and matplotlib. PyMuPDF/pypdf are used for export QA.
Example: python scripts/export_visual_gallery_pdf.py
"""
import hashlib
import html
import io
import json
import math
import os
from pathlib import Path
import re
import time

from PIL import Image as PILImage
from matplotlib import font_manager
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, Image, NextPageTemplate, PageBreak, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/B/initial_audit/NINE_EXPERIMENTS_VISUAL_REVIEW.md'
OUTPUT = ROOT / 'artifacts/figures/NINE_EXPERIMENTS_VISUAL_REVIEW.pdf'
PAGE_W, PAGE_H = landscape(A3)
MARGIN = 38
WIDTH = PAGE_W - 2*MARGIN
FIGURE_HEIGHT = PAGE_H - 230


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inline(value):
    """Render simple inline Markdown as selectable text, with escaped equations."""
    value=value.replace('\u2011','-').replace('\u2013','-').replace('\u2014','-')
    value=html.escape(value)
    value=re.sub(r'`([^`]+)`',r'<font name="GalleryMono">\1</font>',value)
    value=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',value)
    def link(match):
        label,href=match.groups()
        if not href.startswith(('https:','http:','#')):
            href=os.path.relpath((SOURCE.parent/html.unescape(href)).resolve(),OUTPUT.parent)
        return f'<a href="{html.escape(href,quote=True)}" color="#165b85">{label}</a>'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,value)


class GalleryPDF(BaseDocTemplate):
    def afterFlowable(self,flowable):
        if isinstance(flowable,Paragraph) and flowable.style.name in {'GalleryH1','GalleryH2'}:
            title=flowable.getPlainText()
            self._bookmark_count=getattr(self,'_bookmark_count',0)+1
            key='section_'+str(self._bookmark_count)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title,key,level=0,closed=False)


def footer(canvas,doc):
    canvas.saveState()
    canvas.setFont('Gallery',8)
    canvas.setFillColor(colors.HexColor('#566573'))
    canvas.drawString(MARGIN,20,'Experiment B | Training-only visual audit | Markdown export; no new analysis')
    canvas.drawRightString(PAGE_W-MARGIN,20,f'Page {doc.page}')
    canvas.restoreState()


def image_parts(path):
    """Tile at white gutters where possible; retain all pixels and 24px overlap."""
    img=PILImage.open(path).convert('RGB')
    max_pixels=int(FIGURE_HEIGHT*img.width/WIDTH)
    if img.height<=max_pixels:
        return [(0,img.height)]
    import numpy as np
    white=(np.asarray(img).min(axis=2)>249).all(axis=1)
    cuts=[0]
    while img.height-cuts[-1]>max_pixels:
        start=cuts[-1]
        remaining=img.height-start
        count=math.ceil(remaining/(max_pixels-24))
        target=start+remaining/count
        minimum=start+int(max_pixels*.35)
        maximum=start+max_pixels-24
        candidates=[]
        for y in range(minimum,maximum):
            # Leave enough blank gutter for the overlap, avoiding clipped duplicate labels.
            if white[max(0,y-20):y+21].all():
                candidates.append(y)
        cuts.append(min(candidates,key=lambda y:abs(y-target)) if candidates else int(target))
    cuts.append(img.height)
    return [(max(0,a-12 if a else 0),min(img.height,b+12)) for a,b in zip(cuts[:-1],cuts[1:])]


def main():
    wall=time.perf_counter()
    for name,family,weight in [('Gallery','DejaVu Sans','normal'),('GalleryBold','DejaVu Sans','bold'),
                               ('GalleryMono','DejaVu Sans Mono','normal')]:
        path=font_manager.findfont(font_manager.FontProperties(family=family,weight=weight))
        pdfmetrics.registerFont(TTFont(name,path))
    pdfmetrics.registerFontFamily('Gallery',normal='Gallery',bold='GalleryBold',italic='Gallery',boldItalic='GalleryBold')
    body=ParagraphStyle('GalleryBody',fontName='Gallery',fontSize=10.5,leading=15,spaceAfter=10,
                        textColor=colors.HexColor('#182b36'),splitLongWords=True)
    styles={1:ParagraphStyle('GalleryH1',parent=body,fontName='GalleryBold',fontSize=24,leading=31,spaceAfter=20),
            2:ParagraphStyle('GalleryH2',parent=body,fontName='GalleryBold',fontSize=17,leading=23,spaceBefore=12,spaceAfter=14,keepWithNext=True),
            3:ParagraphStyle('GalleryH3',parent=body,fontName='GalleryBold',fontSize=12,leading=17,spaceBefore=10,spaceAfter=8,keepWithNext=True)}
    cell=ParagraphStyle('GalleryCell',parent=body,fontSize=8.5,leading=12,spaceAfter=0)
    story=[];images=[];paragraphs=[];section='';lines=SOURCE.read_text().splitlines();i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:
            i+=1;continue
        heading=re.match(r'^(#{1,3}) (.+)',line)
        if heading:
            level=len(heading[1]);title=heading[2]
            if level==2:
                section=title
                if re.match(r'^(A[2-6]|B[1-3]|C1) ',title):
                    story.append(PageBreak())
            # Figure heading/image/caption form one explicitly paginated plate.
            if level==3 and title.startswith('Figure '):
                j=i+1
                while j<len(lines) and not lines[j].strip(): j+=1
                match=re.match(r'!\[([^\]]*)\]\(([^)]+)\)',lines[j].strip())
                if not match: raise ValueError(f'Figure lacks image: {title}')
                path=(SOURCE.parent/match[2]).resolve()
                k=j+1;caption=[]
                while k<len(lines) and not lines[k].startswith('#'):
                    if lines[k].strip():caption.append(lines[k].strip())
                    k+=1
                parts=image_parts(path);original=PILImage.open(path).convert('RGB')
                images.append(dict(path=path.relative_to(ROOT).as_posix(),sha256=digest(path),
                                   width=original.width,height=original.height,parts=parts))
                for part,(top,bottom) in enumerate(parts):
                    story.append(PageBreak())
                    suffix=f' (part {part+1}/{len(parts)})' if len(parts)>1 else ''
                    story.append(Paragraph(inline(section),styles[3]))
                    story.append(Paragraph(inline(title+suffix),styles[3]))
                    tile=original.crop((0,top,original.width,bottom))
                    memory=io.BytesIO();tile.save(memory,format='PNG');memory.seek(0)
                    scale=min(WIDTH/tile.width,FIGURE_HEIGHT/tile.height)
                    story.append(Image(memory,width=tile.width*scale,height=tile.height*scale,hAlign='CENTER'))
                    if len(parts)>1:
                        story.append(Paragraph(f'Figure continued at original label scale; image rows {top}-{bottom} of {original.height}. Adjacent parts overlap; no content omitted.',cell))
                    if part==len(parts)-1:
                        story.append(Spacer(1,8));story.append(Paragraph(inline(' '.join(caption)),body))
                i=k;continue
            story.append(Paragraph(inline(title),styles[level]));i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                row=[v.strip() for v in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',v) for v in row): rows.append(row)
                i+=1
            count=len(rows[0]);widths=([30,150,100,62,145,117,345,165] if count==8 else
                                    [225,40,76,105,65,110,70,80,145,98] if count==10 else [WIDTH/count]*count)
            widths=[w*WIDTH/sum(widths) for w in widths]
            table=Table([[Paragraph(inline(v),cell) for v in row] for row in rows],colWidths=widths,
                        repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dceaf2')),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f4f7f9')]),
                ('VALIGN',(0,0),(-1,-1),'TOP'),('BOX',(0,0),(-1,-1),.5,colors.HexColor('#b8c9d4')),
                ('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#8ba7b7')),
                ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
                ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
            story.extend([table,Spacer(1,12)]);continue
        paragraph=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','![')):
            paragraph.append(lines[i].strip());i+=1
        text=' '.join(paragraph);paragraphs.append(text);story.append(Paragraph(inline(text),body))
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    if OUTPUT.exists(): raise FileExistsError(f'Preserve existing PDF: {OUTPUT.name}')
    doc=GalleryPDF(str(OUTPUT),pagesize=(PAGE_W,PAGE_H),leftMargin=MARGIN,rightMargin=MARGIN,
                   topMargin=32,bottomMargin=40,title='Experiment B - Initial Visual Audit of Nine Remaining Directions',
                   author='EBMShape research project',pageCompression=1)
    frame=Frame(MARGIN,40,WIDTH,PAGE_H-72,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
    doc.addPageTemplates(PageTemplate(id='gallery',frames=[frame],onPage=footer))
    doc.build(story)
    assert len(images)==44
    manifest=dict(source=SOURCE.relative_to(ROOT).as_posix(),source_sha256=digest(SOURCE),
                  output=OUTPUT.relative_to(ROOT).as_posix(),output_sha256=digest(OUTPUT),
                  bytes=OUTPUT.stat().st_size,unique_figures=len(images),figure_plates=sum(len(x['parts']) for x in images),
                  figures=images,wall_seconds=time.perf_counter()-wall,
                  changes='Presentation export only; original Markdown and figure PNGs unchanged; tall images tiled with overlap')
    OUTPUT.with_suffix('.manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k!='figures'}))


if __name__=='__main__':
    main()
