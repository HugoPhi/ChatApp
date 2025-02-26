.PHONY: all clean

DIR = ./db

# all 目标：运行 python main.py
all: show
	@echo "> Completed"

build:
	@echo "> Running python main.py"
	python main.py

show: build
	@for file in $(shell ls $(DIR)); do \
		echo "> Handling $$file ..."; \
		csvlook "$(DIR)/$$file"; \
		echo "\n"; \
	done

# clean 目标：删除 ./db/
clean:
	@echo "> Cleaning up the ./db/ directory"
	rm -rf ./db/*
