# PBS Alignment  
## LEO Mega Constellations: Congestion, Surveillance, and Governance

**Alignment Identifier:** `PBS-ALIGN-SPJ-LEO-2022-01`

---

## Aligned Work

Zhang, Jingrui, Yifan Cai, Chenbao Xue, Zhirun Xue, and Han Cai.  
“LEO Mega Constellations: Review of Development, Impact, Surveillance, and Governance.”  
*Space: Science & Technology* (a Science Partner Journal), vol. 2022, 2022.  
doi:10.34133/2022/9865174.

---

## Alignment Overview

Zhang et al. review the growth of low Earth orbit (LEO) mega constellations and their effect on astronomical observation, in-orbit spacecraft safety, and the space environment. They conclude that sustaining activity in LEO requires more rational surveillance and governance mechanisms, and examine two responses: space surveillance and situational awareness to keep spacecraft operating safely, and accelerated end-of-life deorbiting through post-mission disposal and active removal.

PBS does not perform surveillance, collision avoidance or debris removal. It defines message formats for authority, position and priority information exchanged between independently operated systems.

---

## Alignment Dimensions

### Congestion and In-Orbit Safety

The paper finds that unrestrained constellation deployment strains orbital resources, increases congestion in LEO and seriously affects the safety of in-orbit operations of many space assets.

**PBS alignment:**  
PBS-AUTH-01 carries authority and scope context, so a message exchanged between independently operated systems states the administrative domain and role under which it was issued.

**Alignment Reference:** `PBS-ALIGN-SPJ-LEO-MULTI-01`

---

### Space Surveillance and Situational Awareness

The paper identifies space surveillance and situational awareness as one of the two main responses to congestion.

**PBS alignment:**  
PBS defines position and presence signaling (PBS-POS-01) bound to an explicit reference frame and time reference (PBS-PNT-CTX-01; PBS-PNT-REQ-001, PBS-PNT-REQ-002).

**Alignment Reference:** `PBS-ALIGN-SPJ-LEO-SSA-02`

---

### Safety-Critical Data

The paper analyses the impact of mega constellations on spacecraft safety in orbit.

**PBS alignment:**  
PBS-PRIO-01 Section 4 defines five priority classes, from 0 CRITICAL (life- or safety-critical data) to 4 BULK, carried in the envelope header independently of transport.

**Alignment Reference:** `PBS-ALIGN-SPJ-LEO-PRIO-03`

---

### Surveillance and Governance Mechanisms

The paper states that space environment stability in LEO must be maintained through more rational surveillance and governance mechanisms.

**PBS alignment:**  
PBS-GOV-01 Sections 2 and 3 separate stewardship of the PBS specifications from commercial implementation, and the specifications are public under the Apache License 2.0.

**Alignment Reference:** `PBS-ALIGN-SPJ-LEO-GOV-04`

---

## Alignment Summary

Zhang et al. find that sustainable LEO activity requires more rational surveillance and governance mechanisms, and review space surveillance, situational awareness and end-of-life deorbiting as responses. PBS defines message formats for the information such coordination exchanges: authority context (PBS-AUTH-01), position with explicit reference frame and time (PBS-POS-01, PBS-PNT-CTX-01) and priority (PBS-PRIO-01).

---

## Citation (MLA)

Zhang, Jingrui, et al. “LEO Mega Constellations: Review of Development, Impact, Surveillance, and Governance.” *Space: Science & Technology*, vol. 2022, 2022, doi:10.34133/2022/9865174.
