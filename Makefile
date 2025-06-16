run-mcp:
	uvicorn src.website.mcp.main:app --reload

run-django:
	python src/website/manage.py runserver 