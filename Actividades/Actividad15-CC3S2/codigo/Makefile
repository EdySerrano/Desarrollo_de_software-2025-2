## Makefile

.PHONY: release

## Creara un tag de release y hacer push de tags.
# make release VERSION=1.1.0
release:
	@if [ -z "$(VERSION)" ]; then \
		echo "Exporta VERSION o usa: make release VERSION=1.2.3"; exit 1; \
	fi
	@git tag -a v$(VERSION) -m "Release $(VERSION)"
	@git push --tags
