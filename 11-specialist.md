# Specialist frontend — WebRTC · Electron · WebGL · AR/Wear · Email · GraphQL federation

12-year architect Q&A for RFP niches. Notebooks: [41](../frontend/41-webrtc-realtime-media/README.md)–[46](../frontend/46-graphql-federation/README.md). DSA: light — see [06](06-dsa-leetcode.md) specialist row.

---

**1. WebSocket vs WebRTC?**  
WS = reliable app messages. WebRTC = media/data with ICE/DTLS; needs signaling + often TURN. Fail: “realtime = WebRTC” for chat badges.

**2. When SFU vs mesh?**  
Mesh only tiny N. Classes/meetings → SFU (LiveKit/mediasoup/cloud). Fail: 20-way mesh on mobile.

**3. TURN cost?**  
Relay bandwidth when P2P fails — budget it or calls die on corporate NAT. Fail: STUN-only in SoW.

**4. Recording a call?**  
Consent, server ingest, retention, residency — not infinite local blobs. Fail: silent record.

**5. Electron security baseline?**  
`contextIsolation`, no `nodeIntegration` in renderer, IPC as API, code sign + notarize. Fail: XSS → RCE.

**6. Electron vs Tauri vs PWA?**  
PWA if URL enough; Electron/Tauri when install/OS APIs required; Tauri if team accepts Rust shell. Fail: Electron to avoid CWV work.

**7. When WebGL?**  
After DOM/Canvas2D prove insufficient (huge viz, 3D). Plan a11y + context-loss. Fail: WebGL login form.

**8. WebGPU?**  
Next GPU API — check support; don’t bet regulated kiosks on it yet.

**9. ARKit/ARCore in enterprise?**  
Native/Unity-shaped; device matrix is the product; camera privacy. Fail: WebXR as warehouse default.

**10. Watch app for approvals?**  
Glance + notify + confirm; money/leave SoR on server; often open phone for step-up. Fail: full CRM on watchOS.

**11. HTML email vs React DS?**  
Separate template stack (tables/MJML); multipart MIME; ESP + webhooks; outbox sends. Fail: reuse Flexbox components in Outlook.

**12. Transactional vs marketing email?**  
Transactional = domain events + idempotency. Marketing = consent + unsubscribe. Fail: password reset via blast tool only.

**13. GraphQL federation when?**  
Multiple **owning** teams + shared types + registry. Else BFF/single schema. Fail: federation day one for one squad.

**14. Federation vs BFF?**  
BFF shapes one client family; federation composes many subgraphs for many clients. Mobile often wants BFF DTOs. Fail: unbounded graph to iOS.

**15. N+1 and authz in GraphQL?**  
DataLoader/batch; per-field authz; depth/complexity limits; persisted queries in enterprise. Fail: raw ORM graph.

**16. Supergraph as SoR?**  
Never — composition/read API. Writes go to domain services with transactions. Fail: resolver dual-write without outbox.

**17. 90s close?**  
“Specialist channels are still clients. WebRTC needs TURN/SFU; Electron needs isolation and signing; WebGL is measured escalation; AR/wear are native-shaped; email is a hostile runtime; federation is an org decision. SoR stays on the server.”

**Next:** [02-frontend](02-frontend.md) · [06 DSA](06-dsa-leetcode.md) · [07 enterprise](07-enterprise.md)
