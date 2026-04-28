<figure markdown="span">
  ![Metaseed](images/metaseed-logo-400.png){ width="200" }
</figure>

# Metaseed

Metaseed provides tools for creating, editing, and validating experimental metadata following MIAPPE (Minimum Information About Plant Phenotyping Experiments) standards.

Metadata structure is defined in YAML specification files, which are used to generate Pydantic models at runtime. This schema-driven approach allows the same codebase to support multiple metadata standards. Fields reference real ontologies (PPEO, ISA, PROV-O) for semantic interoperability.

The library can be used through a command-line interface, a web-based editor, or programmatically via Python.
