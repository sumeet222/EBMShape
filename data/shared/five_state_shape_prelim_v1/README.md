# Five preliminary screens: private shared inputs

The observed market extracts, published workbook, HTML release metadata and compact
shared derivatives in this directory are local research inputs, excluded from Git.
They are not included in the review ZIP. No raw input is duplicated in an experiment.

The exact source, revision, SHA-256, schema, timestamp convention and permission
limitations are recorded in `artifacts/five_state_shape_prelim_v1/manifests/` from the
repository root. See `source_registry.json`, `union_acquisition_plan.json`,
`acquired_sources.json` and `validated_inputs.json`. Minute OHLCV uses UTC bar starts;
the derived event/return variables are explicitly defined in the last manifest.

Reproduction requires authorized access to the frozen local SPY training-era graph,
the original ten-stock observed30-minute files, and the cached observed BAC/KO2019
partitions. External roots can be configured with `PRELIM_SAE_ROOT` and
`PRELIM_LSTM_ROOT`; never copy filled/indicator datasets into these paths. A public
clone does not supply those private inputs. Restore exact hashes, not similarly named
files. The HF minute source is authorized for this private preliminary screen; upstream
vendor rights are not independently certified, and redistribution is not authorized.

On a fresh clone install the package with the existing `stage1_5` extra and versions
in the run's `runtime_environment.json`. For an exact run, use Python3.14.6 and the
recorded versions. Then restore authorized hash-matching inputs into the documented
relative locations, and run `python -B scripts/five_prelim.py derive`, `screen`,
`report`, `verify`. A restored completed run uses `screen`/`verify` to validate or
skip checkpoints; it must not run `inventory`/`freeze` over an existing frozen run.
The acquisition CLI is resumable and validates each month before skipping it;
do not run a second archive pass or change the selected2019union. If essential
private inputs cannot be restored, preserve DATA HOLD rather than substitute data.
