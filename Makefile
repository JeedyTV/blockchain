.PHONY = help clean vsopc

help:
	@echo "---------------HELP-----------------"
	@echo "To setup the project type make vsopc"
	@echo "To install tools type make install-tools"
	@echo "To know how to use the compiler vsopc: type ./vsopc -h"
	@echo "------------------------------------"

install-tools:
	@echo "installing tools ..."
	@pip install -r requirements.txt

comp:
	@echo "archive made ..."
	@./make_archive.sh	

run:
	@cls
	@python app.py --p 5000 --m True
	@python app.py --p 20000 --m False --b localhost:5000

clean:
	@echo "cleaned"
	@rm -f -r __pycache__
	@rm -f vsopc
	@rm -f -r .vscode
	@rm vsopcompiler.tar.xz