# ISA and MIAPPE Comparison

This document compares the ISA (Investigation-Study-Assay) and MIAPPE (Minimum Information About Plant Phenotyping Experiments) metadata standards, highlighting their shared concepts and domain-specific extensions.

## Overview

Both standards follow a hierarchical structure for organizing experimental metadata:

- **ISA**: General-purpose framework for life science experiments, with emphasis on assay workflows and data provenance
- **MIAPPE**: Plant phenotyping-specific standard, with emphasis on field trials, germplasm, and environmental conditions

## Entity Comparison Diagram

```mermaid
flowchart TB
    subgraph shared["Shared Concepts"]
        direction TB
        INV[Investigation]
        STU[Study]
        PER[Person/Contact]
        PUB[Publication]
        SAM[Sample]
        FAC[Factor]
        FV[FactorValue]
        DF[DataFile]
    end

    subgraph isa["ISA-Specific"]
        direction TB
        ASS[Assay]
        PROT[Protocol]
        PP[ProtocolParameter]
        SRC[Source]
        EXT[Extract]
        LEXT[LabeledExtract]
        PROC[Process]
        OA[OntologyAnnotation]
        OS[OntologySource]
        CHAR[Characteristic]
        PV[ParameterValue]
        COM[Comment]
    end

    subgraph miappe["MIAPPE-Specific"]
        direction TB
        BM[BiologicalMaterial]
        OU[ObservationUnit]
        OV[ObservedVariable]
        EVT[Event]
        ENV[Environment]
        LOC[Location]
        MS[MaterialSource]
    end

    %% Shared relationships
    INV --> STU
    INV --> PER
    INV --> PUB
    STU --> SAM
    STU --> FAC
    FAC --> FV

    %% ISA relationships
    STU --> ASS
    ASS --> DF
    STU --> PROT
    PROT --> PP
    STU --> SRC
    SRC --> SAM
    SAM --> EXT
    EXT --> LEXT
    PROC --> PV
    ASS --> PROC

    %% MIAPPE relationships
    STU --> BM
    STU --> OU
    STU --> OV
    STU --> EVT
    STU --> ENV
    STU --> LOC
    BM --> MS
    OU --> SAM

    %% Styling
    classDef shared fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
    classDef isa fill:#e3f2fd,stroke:#2196f3,stroke-width:2px
    classDef miappe fill:#fff3e0,stroke:#ff9800,stroke-width:2px

    class INV,STU,PER,PUB,SAM,FAC,FV,DF shared
    class ASS,PROT,PP,SRC,EXT,LEXT,PROC,OA,OS,CHAR,PV,COM isa
    class BM,OU,OV,EVT,ENV,LOC,MS miappe
```

## Detailed Comparison

### Shared Core Entities

| Concept | ISA | MIAPPE | Notes |
|---------|-----|--------|-------|
| **Investigation** | `Investigation` | `Investigation` | Top-level container for studies |
| **Study** | `Study` | `Study` | Central experimental unit |
| **Person** | `Person` (last_name, first_name) | `Person` (name) | Contact information; ISA splits name fields |
| **Publication** | `Publication` | via `associated_publications` | ISA has structured entity; MIAPPE uses DOI list |
| **Sample** | `Sample` | `Sample` | Material sampled from subjects |
| **Factor** | `StudyFactor` | `Factor` | Independent variables |
| **FactorValue** | `FactorValue` | `FactorValue` | Specific factor levels |
| **DataFile** | `DataFile` | `DataFile` | Output data files |

### ISA-Specific Entities

| Entity | Purpose |
|--------|---------|
| **Assay** | Measurement/test performed on samples; links technology to data |
| **Protocol** | Detailed experimental procedures with parameters |
| **Source** | Original biological material before processing |
| **Extract** | Material extracted from samples |
| **LabeledExtract** | Labeled material for detection |
| **Process** | Nodes in experimental workflow graph |
| **OntologyAnnotation** | Structured ontology term references |
| **Characteristic** | Material property qualifiers |

### MIAPPE-Specific Entities

| Entity | Purpose |
|--------|---------|
| **BiologicalMaterial** | Germplasm/plant material with accession info |
| **ObservationUnit** | Plot, plant, or pot being measured |
| **ObservedVariable** | Trait + Method + Scale (measurement definition) |
| **Event** | Discrete occurrences (sowing, harvest, treatment) |
| **Environment** | Environmental parameter recordings |
| **Location** | Geographic site information |
| **MaterialSource** | Genebank or institution providing material |

## Structural Differences

```mermaid
flowchart LR
    subgraph isa_flow["ISA: Process-Centric"]
        S1[Source] --> P1[Process] --> S2[Sample]
        S2 --> P2[Process] --> E1[Extract]
        E1 --> P3[Process] --> D1[Data]
    end

    subgraph miappe_flow["MIAPPE: Observation-Centric"]
        BM1[BiologicalMaterial] --> OU1[ObservationUnit]
        OU1 --> OBS[Observations]
        OBS --> VAR[ObservedVariable]
        EVT1[Events] --> OU1
        ENV1[Environment] --> OU1
    end
```

### ISA Approach
- Models experiments as **directed acyclic graphs** of processes
- Tracks material transformations (Source -> Sample -> Extract -> Data)
- Protocol-centric: every transformation references a protocol
- Supports complex multi-omics workflows

### MIAPPE Approach
- Models experiments as **observation units** with measurements
- Field trial-oriented: plots, blocks, replicates
- Trait-centric: measurements defined by trait/method/scale
- Includes environmental and event tracking

## Mapping Between Standards

When converting between ISA and MIAPPE:

| ISA Concept | MIAPPE Equivalent | Mapping Notes |
|-------------|-------------------|---------------|
| Source | BiologicalMaterial | ISA Source ~ MIAPPE germplasm |
| Sample | Sample or ObservationUnit | Depends on context |
| Assay | Study + ObservedVariable | MIAPPE doesn't separate assays |
| Protocol | Event or cultural_practices | Less structured in MIAPPE |
| Characteristic | BiologicalMaterial fields | Organism, genus, species, etc. |
| Process | Event | MIAPPE events are simpler |

## When to Use Each Standard

**Use ISA when:**

- Working with multi-omics data (genomics, proteomics, metabolomics)
- Need detailed protocol documentation
- Tracking complex sample processing workflows
- Integrating with ISA-Tab ecosystem tools

**Use MIAPPE when:**

- Conducting plant phenotyping experiments
- Managing field trial data
- Need germplasm/accession tracking
- Working with BrAPI-compatible systems
- Environmental data is important

## References

- [ISA Framework](https://isa-tools.org/)
- [ISA-Tab Specification](https://isa-specs.readthedocs.io/)
- [MIAPPE Standard](https://www.miappe.org/)
- [MIAPPE v1.1 Checklist](https://github.com/MIAPPE/MIAPPE/tree/master/MIAPPE_Checklist-Data-Model-v1.1)
