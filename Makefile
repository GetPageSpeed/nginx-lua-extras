.PHONY: all
all:clean
	./generate-definitions.py
	./generate.sh

.PHONY: clean
clean:
	rm -rf resty/*.yml *.spec
