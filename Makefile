.PHONY: test
test:
	python manage.py test --settings=rest_scheduler.settings.test

.PHONY: coverage
coverage:
	coverage run --source='.' manage.py test --settings=rest_scheduler.settings.test && coverage report -m