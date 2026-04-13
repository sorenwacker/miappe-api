# ISA-MIAPPE-Combined

The combined profile merges ISA and MIAPPE into a single coherent model. This is useful for plant science experiments that involve both phenotyping (field measurements, growth observations) and molecular assays (genomics, transcriptomics, metabolomics).

Entities that exist in both standards (Investigation, Study, Person, Sample, Factor) are unified with a shared definition. ISA-specific entities (Assay, Protocol, Process) and MIAPPE-specific entities (BiologicalMaterial, ObservationUnit, ObservedVariable) are both available.

Two versions are available: v1.0 provides a straightforward merge, while v2.0 introduces an Experiment entity for multi-trial studies and uses a reference-based ownership model.

## v1.0

Version 1.0 contains 25 entities with a flat ownership model where Study directly owns most child entities.

```mermaid
flowchart TB
    subgraph shared["Shared Core (7)"]
        INV[Investigation]
        STU[Study]
        PER[Person]
        SAM[Sample]
        FAC[Factor]
        FV[FactorValue]
        DF[DataFile]
    end

    subgraph isa["ISA Extensions (12)"]
        ASS[Assay]
        PROT[Protocol]
        PP[ProtocolParameter]
        SRC[Source]
        EXT[Extract]
        LEXT[LabeledExtract]
        PROC[Process]
        PV[ParameterValue]
        CHAR[Characteristic]
        PUB[Publication]
        OA[OntologyAnnotation]
        OS[OntologySource]
    end

    subgraph miappe["MIAPPE Extensions (6)"]
        BM[BiologicalMaterial]
        OU[ObservationUnit]
        OV[ObservedVariable]
        EVT[Event]
        ENV[Environment]
        MS[MaterialSource]
    end

    INV --> STU
    INV --> PER
    INV --> PUB
    STU --> ASS
    STU --> PROT
    STU --> SRC
    STU --> FAC
    STU --> BM
    STU --> OU
    STU --> OV
    STU --> EVT
    STU --> ENV
    PROT --> PP
    SRC -->|Process| SAM
    SAM -->|Process| EXT
    EXT -->|Process| LEXT
    ASS --> PROC
    ASS --> DF
    PROC --> PV
    FAC --> FV
    OU --> SAM
    BM --> MS

    classDef shared fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
    classDef isa fill:#e3f2fd,stroke:#2196f3,stroke-width:2px
    classDef miappe fill:#fff3e0,stroke:#ff9800,stroke-width:2px

    class INV,STU,PER,SAM,FAC,FV,DF shared
    class ASS,PROT,PP,SRC,EXT,LEXT,PROC,PV,CHAR,PUB,OA,OS isa
    class BM,OU,OV,EVT,ENV,MS miappe
```

---

## v2.0

Version 2.0 introduces the **Experiment** entity for studies that span multiple trials, locations, or time periods. A Study owns shared resources (biological materials, observation units, protocols) while Experiments reference these resources and own time/location-specific data (events, environments, assays).

This reference-based model avoids duplicating entity definitions across experiments while maintaining clear ownership.

```mermaid
flowchart TB
    subgraph shared["Shared Core (7)"]
        INV[Investigation]
        STU[Study]
        EXP[Experiment]
        PER[Person]
        PUB[Publication]
        FAC[Factor]
        FV[FactorValue]
    end

    subgraph isa["ISA Extensions (9)"]
        ASS[Assay]
        PROT[Protocol]
        PP[ProtocolParameter]
        PROC[Process]
        PV[ParameterValue]
        SRC[Source]
        SAM[Sample]
        EXT[Extract]
        LEXT[LabeledExtract]
    end

    subgraph miappe["MIAPPE Extensions (5)"]
        BM[BiologicalMaterial]
        OU[ObservationUnit]
        OV[ObservedVariable]
        EVT[Event]
        ENV[Environment]
    end

    subgraph annotations["Shared Annotations (3)"]
        OA[OntologyAnnotation]
        OS[OntologySource]
        CHAR[Characteristic]
    end

    subgraph support["Support (2)"]
        MS[MaterialSource]
        DF[DataFile]
    end

    INV --> STU
    INV --> PER
    INV --> PUB
    STU --> EXP
    STU --> PROT
    STU --> FAC
    STU --> BM
    STU --> OU
    STU --> OV
    STU --> SAM
    EXP --> ASS
    EXP --> EVT
    EXP --> ENV
    EXP -.->|references| OU
    EXP -.->|references| SAM
    PROT --> PP
    SRC -->|Process| SAM
    SAM -->|Process| EXT
    EXT -->|Process| LEXT
    ASS --> PROC
    ASS --> DF
    PROC --> PV
    FAC --> FV
    BM --> MS

    classDef shared fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
    classDef isa fill:#e3f2fd,stroke:#2196f3,stroke-width:2px
    classDef miappe fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    classDef annot fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px
    classDef supp fill:#eceff1,stroke:#607d8b,stroke-width:2px

    class INV,STU,EXP,PER,PUB,FAC,FV shared
    class ASS,PROT,PP,PROC,PV,SRC,SAM,EXT,LEXT isa
    class BM,OU,OV,EVT,ENV miappe
    class OA,OS,CHAR annot
    class MS,DF supp
```

### v2.0 Ownership Model

```mermaid
flowchart LR
    subgraph study["Study OWNS (shared pool)"]
        direction TB
        BM[BiologicalMaterials]
        OU[ObservationUnits]
        SAM[Samples]
        OV[ObservedVariables]
        FAC[Factors]
        PROT[Protocols]
    end

    subgraph exp["Experiment OWNS (time/location specific)"]
        direction TB
        EVT[Events]
        ENV[Environments]
        ASS[Assays]
    end

    exp -.->|observation_unit_ids| OU
    exp -.->|sample_ids| SAM

    classDef owns fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
    classDef refs fill:#fff3e0,stroke:#ff9800,stroke-width:2px

    class BM,OU,SAM,OV,FAC,PROT owns
    class EVT,ENV,ASS refs
```

## v2.0 Changes from v1.0

| Change | Description |
|--------|-------------|
| **New Experiment entity** | For multi-trial studies within a Study |
| **Person** | Unified naming (`given_name`/`family_name`) |
| **Publication** | Promoted to shared core |
| **Reference model** | Experiment references Study's entities by ID |

## Usage

```python
from metaseed.facade import ProfileFacade

# v2.0 (recommended)
combined = ProfileFacade("isa-miappe-combined", "2.0")

# Both ISA and MIAPPE entities available
protocol = combined.Protocol(name="RNA Extraction")
material = combined.BiologicalMaterial(identifier="BM-001", organism="Zea mays")
experiment = combined.Experiment(identifier="EXP-001", observation_unit_ids=["OU-001"])

# v1.0
combined_v1 = ProfileFacade("isa-miappe-combined", "1.0")
```
