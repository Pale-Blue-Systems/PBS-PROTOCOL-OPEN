# PBS-REFERENCES-RESOURCES.md  
## References, Standards, and Supporting Resources

**Status:** Informational  
**Applies to:** Pale Blue Systems Open Standard (PBS)

---

## 1. Purpose

This document lists the external standards, agency documents and programs that the PBS specifications build on, map to, or address. It falls into three categories:

1. **Networking protocols and standards** that PBS is carried over or maps to
2. **Agency need statements and specifications** that PBS v1.4 traces to
3. **Programs, missions, and initiatives**—public and commercial—that demonstrate the relevance and necessity of PBS-style solutions  

All links reference publicly available, validated sources. Each link was checked on 2026-10-06.

---

## 2. Networking Protocols and Standards

### Delay/Disruption Tolerant Networking (DTN)

- **RFC 4838 – Delay-Tolerant Networking Architecture** (Informational, April 2007)  
  https://datatracker.ietf.org/doc/html/rfc4838  

- **RFC 9171 – Bundle Protocol Version 7 (BPv7)** (Proposed Standard, January 2022)  
  https://datatracker.ietf.org/doc/html/rfc9171  
  Section 4.2.6 defines DTN time as milliseconds since 2000-01-01 00:00:00 UTC; Section 4.3.1 defines bundle lifetime in milliseconds past the creation time.

- **RFC 9172 – Bundle Protocol Security (BPSec)** (Proposed Standard, January 2022)  
  https://www.rfc-editor.org/rfc/rfc9172  

- **RFC 5326 – Licklider Transmission Protocol (LTP) Specification** (Experimental, September 2008)  
  https://www.rfc-editor.org/rfc/rfc5326  

- **RFC 5050 – Bundle Protocol Specification** (Experimental, November 2007; the specification RFC 9171 was adapted from)  
  https://datatracker.ietf.org/doc/html/rfc5050  

- **IETF Delay/Disruption Tolerant Networking (dtn) Working Group**  
  https://datatracker.ietf.org/wg/dtn/about/  

PBS-DTN-MAP-01 and PBS-DTN-MAP-02 define PBS carriage over BPv7. Within PBS-native domains, DTN wrapping is not required (PBS-DTN-MAP-01 Section 2).

---

### CCSDS (Consultative Committee for Space Data Systems)

- **CCSDS Blue Books (Recommended Standards)**  
  https://ccsds.org/publications/bluebooks/  

- **CCSDS 730.1-G-1 – Solar System Internetwork (SSI) Architecture** (Informational Report, July 2014)  
  https://ccsds.org/Pubs/730x1g1.pdf  

- **CCSDS 730.2-G-1 – Concepts and Rationale for Streaming Services over Bundle Protocol** (Informational Report, September 2018)  
  https://ccsds.org/Pubs/730x2g1.pdf  

LNIS V005 Section 3.1.2 cites the CCSDS profile of BPv7, CCSDS 734.2-P-1.1 (draft Recommended Standard), as applicable document [AD19].

CCSDS standards form the backbone of interoperable space communications across international agencies.

---

## 3. DTN Implementations

### Interplanetary Overlay Network (ION)

ION is the open-source DTN implementation developed by NASA's Jet Propulsion Laboratory.

ION is NASA/JPL’s reference implementation of DTN for space missions.

- **ION-DTN repository (nasa-jpl)**  
  https://github.com/nasa-jpl/ION-DTN  

PBS-DTN-MAP-01 Section 11 names ION as an example of NASA DTN infrastructure. Templin et al., “High Performance DTN Using Larger Packets and Kernel Resident Convergence Layers”, 2025 IEEE Aerospace Conference, doi:10.1109/AERO63441.2025.11068517 (`PBS-ALIGN-IEEE-AEROCONF-2025-01`), report ION and NASA Glenn HDTN throughput over LTP.

ION demonstrates operational DTN across flight and ground systems and serves as a primary interoperability target for PBS-DTN-MAP.

---

### NASA Space Communications and Navigation (SCaN)

- **SCaN: Communicating with Missions**  
  https://www.nasa.gov/communicating-with-missions/  

- **NASA Delay/Disruption Tolerant Networking**  
  https://www.nasa.gov/communicating-with-missions/delay-disruption-tolerant-networking/  

These efforts validate DTN as a critical component of future space architectures.

---

## 4. NASA Need Statements and LunaNet

### FY26 Civil Space Shortfall Prioritization

- **NASA STMD, *FY26 Civil Space Shortfall Prioritization*** (May 2026)  
  https://www.nasa.gov/wp-content/uploads/2026/05/fy26-civil-space-shortfall-prioritization.pdf  

- **NASA, *2026 Civil Space Shortfalls*** (released 12 January 2026)  
  https://www.nasa.gov/wp-content/uploads/2026/03/2026-civil-space-shortfalls.pdf  

- **NASA, *2026 Civil Space Shortfall Ranking*** (call for stakeholder feedback, 12 January – 20 February 2026)  
  https://www.nasa.gov/directorates/stmd/prizes-challenges-crowdsourcing-program/center-of-excellence-for-collaborative-innovation-coeci/2026-civil-space-shortfall-ranking/  

This document identifies technology gaps requiring development to support future exploration, including communications, autonomy, and distributed systems.

The prioritization defines a shortfall as “a technology area requiring further development to meet future exploration, science, and other mission needs”, consolidates the shortfalls into 32 categories, and ranks them. PBS v1.4 traces to need statements 13.09, 15.01, 15.03 and 24.05 (`PBS-TRACE-NASA-FY26-01`; texts quoted in `PBS-ALIGN-NASA-LCRNS-02`).

---

### LunaNet and LCRNS

- **NASA, ESA, and JAXA, *LunaNet Interoperability Specification Document*, Version 5 (LNIS V005)** (Baseline, 29 January 2025)  
  https://www.nasa.gov/wp-content/uploads/2025/02/lunanet-interoperability-specification-v5-baseline.pdf  

- **NASA, LunaNet Interoperability Specification page**  
  https://www.nasa.gov/directorates/somd/space-communications-navigation-program/lunanet-interoperability-specification/  

- **NASA Goddard Exploration and Space Communications, LCRNS**  
  https://www.nasa.gov/goddard/esc/lcrns/  

PBS-LNIS-01 defines PBS operation over LunaNet IP and BPv7 network services.

---

### Moon to Mars Architecture

- **NASA Moon to Mars Architecture**  
  https://www.nasa.gov/moontomarsarchitecture/  

The Moon to Mars strategy explicitly depends on interoperable, extensible, and evolvable communications spanning Earth, lunar, and Mars domains.

---

## 5. Related NASA Programs

### Lunar and Cislunar

- **NASA Artemis**  
  https://www.nasa.gov/humans-in-space/artemis/  

- **Gateway**  
  https://www.nasa.gov/mission/gateway/  

These programs involve distributed systems, multiple partners, and intermittent connectivity—conditions PBS is designed to address.

- **Commercial Lunar Payload Services (CLPS)**  
  https://www.nasa.gov/commercial-lunar-payload-services/  

- **NASA Commercial Space**  
  https://www.nasa.gov/humans-in-space/commercial-space/  

These initiatives highlight the need for interoperable communication frameworks across multiple independent operators.

---

### Mars and Deep Space

- **NASA Mars Exploration**  
  https://science.nasa.gov/mars/  

- **Deep Space Network (DSN)**  
  https://www.nasa.gov/directorates/somd/space-communications-navigation-program/what-is-the-deep-space-network/  

PBS-PRIO-01 Section 14 gives an informative mapping from DSN priority levels to PBS priority classes. PBS operates at the packet layer within DSN-allocated link time and requires no DSN modification (Section 14.3).

PBS complements DSN and deep-space relay systems by providing a standardized application-layer communication model.

---

## 6. International Space Agencies

- **European Space Agency (ESA)**  
  https://www.esa.int  

- **Japan Aerospace Exploration Agency (JAXA)**  
  https://www.jaxa.jp  

- **Canadian Space Agency (CSA)**  
  https://www.asc-csa.gc.ca  

NASA, ESA and JAXA wrote and approved LNIS V005 (LNIS V005 Section 1.1).

---

## 7. DTN Research

- **IRTF Delay-Tolerant Networking Research Group (DTNRG)** (concluded)  
  https://www.irtf.org/concluded/dtnrg.html  

- **Humanitarian and Disaster Networking (DTN Use Cases)**  
  https://www.ietf.org/proceedings/  

PBS draws on lessons learned from terrestrial DTN deployments in disaster response, remote research, and infrastructure-poor regions.

---

## 8. Open Standards Bodies

- **Internet Engineering Task Force (IETF)**  
  https://www.ietf.org  

- **World Wide Web Consortium (W3C)**  
  https://www.w3.org  

- **Linux Foundation**  
  https://www.linuxfoundation.org  

These organizations maintain open standards or open-source projects under vendor-neutral governance. PBS-GOV-01 defines PBS governance.

---

## 9. Summary

The Pale Blue Systems Open Standard is grounded in:
- established space and networking protocols  
- publicly identified mission needs and technology gaps  
- real-world programs spanning civil, commercial, and international space activity  

PBS builds on this foundation to provide a coherent, interoperable communication layer designed for humanity’s sustained presence beyond Earth.

---

**Pale Blue Systems Foundation**  
Stewarding open, interoperable communication standards for humanity’s future in space.
