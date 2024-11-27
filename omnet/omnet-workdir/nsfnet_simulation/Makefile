all: checkmakefiles
	cd src && $(MAKE)

clean:
	cd src && $(MAKE) clean

cleanall:
	cd src && $(MAKE) MODE=release clean
	cd src && $(MAKE) MODE=debug clean
	rm -f src/Makefile

makefiles:
	cd src && opp_makemake -f --deep \
		-O out \
		-KINET_PROJ=/workdir/inet \
		-DINET_IMPORT \
		-I$(INET_PROJ)/src \
		-L$(INET_PROJ)/out/clang-release/src \
		-lINET

checkmakefiles:
	@if [ ! -f src/Makefile ]; then \
	echo; \
	echo '=== Makefile does not exist. Generate it by running "make makefiles"'; \
	echo; \
	exit 1; \
	fi