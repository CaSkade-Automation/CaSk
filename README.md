# CaSk - A Capability and Skill Ontology Based on Industry Standards

## Introduction
In the context of automated production, Capabilities and Skills are terms that are used to refer to machine functions. A *Capability* is an implementation-independent specification of a function to achieve an effect in the physical or virtual world. A *Capability* may be implemented by one or more *Skills*. Skills are encapsulated implementations with a well-defined invocation interface (e.g., using OPC UA).
Consider a Capability as a machine-interpretable description of a function. Such a description typically features *Properties* and constraints on these properties.

For the terminology around capabilities and skills, an abstract *CSS Reference Model* was defined in a [Plattform Industrie 4.0 Whitepaper](https://www.plattform-i40.de/IP/Redaktion/EN/Downloads/Publikation/CapabilitiesSkillsServices.html) and additionally published in a [scientific publication](https://www.degruyter.com/document/doi/10.1515/auto-2022-0117/html).
This reference model is implemented by the abstract [CSS Ontology](https://github.com/hsu-aut/css-ontology). The CSS ontology covers all terms and relations of the reference model. But these elements are too generic to model specific capabilities and skills. The CSS ontology does not provide possibilities to model capability parameters in the detail or to model skill interfaces in a specific technology.

To be able to model such details, an extension of the CSS model is needed. At the same time, however, this extension of the CSS ontology should not be done on the level of individual domains, because there are certain model elements that are independent of a specific application domain. An "intermediate level" between the abstract CSS ontology and domain-specific ontologies seems reasonable. The CaSk ontology forms exactly this intermediate level. It extends the CSS ontology and at the same time maintains extensibility for domain-specific ontologies.

## Ontology Architecture
<p align="center">
<img src="https://github.com/hsu-aut/cask/blob/documentation/images/images/architecture_marker-cask.jpg?raw=true" width="800" title="CSS Architecture">
</p>

CaSk is part of a three-level ontology architecture. At the top is the CSS ontology with its definitions of terms and their relations. At the bottom are currently two domain-specific ontologies:
- The CaSkMan ontology can be used to model capabilities and skills in manufacturing. It extends CaSk by standards such as DIN 8580 (manufacturing operations), VDI 2860 (handling operations) as well as WADL and OPC UA to model skills with interfaces based on web services as well as OPC UA.
- RoboCaSk is an ontology for capabilities and skills of autonomous systems that can work collaboratively to achieve a common goal. It extends CaSk by additional elements to represent such systems and thei skill interfaces.

And CaSk is right in the middle. It extends the CSS ontology and at the same time maintains extensibility for domain-specific ontologies.


## Extensions to the CSS Ontology

The CaSk ontology makes use of so-called *Ontology Design Patterns* (ODPs), which are self-contained ontologies based on standards. Four ODPs are imported and aligned in CaSk in order to extend the CSS ontology:
- **VDI 3682**: This guideline defines *Formalized Process Description*, a simple means to model processes of all kinds. It defines classes for process, process operator, technical resource as well as inputs and outputs. These classes and the properties of VDI 3682 are used to model the abstract terms process, product and resource of the CSS ontology in more detail. This is done, e.g., by setting `CSS:Process` equivalent to the `VDI3682:Process` and by setting `VDI3682:TechnicalResource` to be a subclass of `CSS:Resource`
- **VDI 2206**: In this guideline, a very simplistic model of a system structure is defined. Systems can be composed of other systems or modules, which can in turn be composed of components. This ODP is used to model resources in more detail. This is achieved by setting both `VDI2206:System` as well as `VDI2206:Module` as subclasses of `VDI3682:TechnicalResource` (and thus also subclasses of `CSS:Resource`)
- **ISA 88**: This ODP contains the state machine according to PackML with all its states and transitions. This `ISA88:StateMachine` is modeled to be a subclass of `CSS:StateMachine` so that state machines of skills can be modeled in great detail.
- **IEC 61360**: IEC 61360 defines a meta model for properties. With this ODP, you can define your own property (types and instances). Types are defined only once so that all instances of a type can refer to this one type definition. Properties according to IEC 61360 can be used to model capability properties but also to express all sorts of things about other model elements (e.g., processes or resources)


## Ontology example
Detailed examples can be found in the two repositories of  [CaSkMan](https://github.com/aljoshakoecher/caskman) and [RoboCaSk](https://github.com/Miguel2617/robocap). Are you interested in a more abstract example using only the CaSk ontology? Feel free to create an issue to let us know. We can provide such an example in the future.
