PYTHON ?= python3

.PHONY: test demo ui

test:
	$(PYTHON) scripts/verify.py

demo:
	$(PYTHON) ai-stack/pipeline/run.py ai-stack/demo_data/incoming/new_rfp.md --provider stub --out ai-stack/out

ui:
	$(PYTHON) ai-stack/ui/app.py
