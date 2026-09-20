# Mobile interview Q&A — React Native · Android · iOS (12-year architect)

Architect bar for **mobile clients**. Phone apps are **clients**; SoR stays on the server. Steal the **question**, not Uber’s stack.

**Chapter:** [frontend 40](../frontend/40-react-native-android-ios/README.md) · [23 PWA](../frontend/23-pwa-mobile-web/README.md) · [38 push](../frontend/38-realtime-sockets-notifications/README.md) · real apps [07](07-enterprise.md).

---

**1. PWA vs React Native vs native — how do you choose?**  
URL-enough (employees, SMS links, SEO): responsive; add PWA for install/offline on Android. Store presence, camera/files/offline-as-core: RN or native. Extreme platform UI/perf or heavy OEM: Kotlin/Swift. Fail: RN because “we know React” with no store/hardware need.

**2. Is React Native free if the web team knows React?**  
No. Yoga, Metro, Hermes, native modules, New Architecture upgrades, App Store/Play trains, and device QA are a **second product**. Fail: “write once” as the ADR.

**3. What do you share between web and RN?**  
BFF/OpenAPI contracts, IdP, design **tokens**, validation types. Not DOM components or cookie assumptions. Fail: one Redux store shared into a WebView.

**4. Expo vs bare RN?**  
Expo/EAS for speed and OTA of **JS**. Plan prebuild/eject when a custom native module appears — ADR the escape **before** the first plugin. Fail: Expo forever with no escape.

**5. New Architecture (Fabric / JSI / TurboModules)?**  
Current RN direction; brownfield may lag. Upgrade is a **programme**, not a weekend. Fail: ignore until a dependency forces a break.

**6. When Kotlin/Swift instead of RN?**  
Platform-first UX, DRM/player, deep background modes, team already native, or RN module tax exceeds two codebases. Fail: “native only” for a CRUD HR app.

**7. Flutter vs RN?**  
Flutter: greenfield, strong custom UI, Dart hiring. RN: React estate and JS hiring. Fail: Flutter to match a React design-system org without Dart bench.

**8. Capacitor/Cordova?**  
Wrap existing web into a store binary. Does not fix a 4 MB INP — you shipped a WebView. Fail: marketing Capacitor as RN.

**9. Mobile BFF — why?**  
Coarse payloads, fewer round-trips, mobile-specific DTOs, auth shape. Don’t force unbounded web GraphQL onto iOS. Fail: 40 chatty REST calls per screen.

**10. Auth on mobile?**  
OIDC + PKCE (AppAuth). Short access token; refresh in **Keychain/Keystore**, not plain AsyncStorage for high-risk. Biometric unlocks the secret — server still AuthZ. Fail: god token in the binary.

**11. Certificate pinning?**  
High-threat apps; you own pin rotation and emergency unpin. Fail: pin without ops story.

**12. Push architecture?**  
Domain event → worker → **FCM** (Android) / **APNs** (iOS). Inbox **SoR** on server for badge rebuild. Sensitive data fetched after unlock. Fail: WebSocket as the only notify when the app is killed.

**13. Open-app realtime vs push?**  
WS/SSE while foreground; push when background/killed. Fail: one mechanism for both.

**14. Offline / field apps?**  
Local DB + **outbox** + idempotent APIs + conflict ADR. Fail: fire-and-forget dual-write to SQLite and API.

**15. Lists and performance?**  
Virtualize (FlashList); measure cold start, JS FPS, ANR on **mid Android** and 4G India. Fail: flagship-only QA.

**16. Deep linking?**  
Universal Links / App Links + navigation config; auth-gated routes; deferred deep link if install required. Fail: custom scheme only with no verification.

**17. Release trains?**  
Internal → TestFlight/closed testing → staged % → prod. Feature flags + force-upgrade for breaking API. Fail: treating mobile like `firebase deploy` for web.

**18. OTA updates?**  
JS-only (EAS Update/CodePush) under policy; native bumps need store review. Fail: OTA a native module change.

**19. IAP / payments?**  
StoreKit / Play Billing rules are **policy**. Real money ledgers stay server-side. Fail: inventing billing only in the client.

**20. MDM / enterprise distribution?**  
Intune etc. may sideload or private store — ask **how employees get the binary** before promising Play. Fail: consumer store assumptions for bank employees.

**21. Observability?**  
Crashlytics/Sentry, ANR, network errors, cold start; scrub PII; correlate `x-request-id` to backend. Fail: console.log tokens.

**22. Account deletion / DPDP?**  
In-app delete and server DSR — store requirement class. Fail: “email support to delete” only.

**23. White-label?**  
Flavors/schemes, separate bundle IDs, IdP per tenant — or one app with runtime config if policy allows. Fail: one binary, wrong logo hard-coded.

**24. Banking / UPI-class?**  
Often native or RN + heavy native; biometrics; no offline money invent. SoR server. Fail: copy social-app offline sync.

**25. HR leave app?**  
Start responsive/PWA; RN only if store/brand/push requirements win TCO. Fail: two native teams for approve/reject.

**26. Insurance FNOL photos?**  
RN/native; camera; offline outbox; blobs to object storage; claim SoR OLTP. Fail: vector DB as claim master.

**27. Netflix-class player?**  
Native players + DRM — steal **constraints**, not your grocery app stack.

**28. Security review leftovers?**  
Root/jailbreak detection is best-effort; App Attest/Play Integrity help; still assume compromised client. Fail: “client validated = safe.”

**29. Monorepo?**  
Tokens + contracts in packages; Metro watch folders; separate versioning for store apps. Fail: one semver for web and iOS binary.

**30. 90s closing?**  
“Clients only. Pick web/PWA/RN/native from distribution and hardware. Share BFF and tokens. Push via FCM/APNs with server inbox. Offline = outbox + idempotency. Store trains on the plan. RN is not free React.”

**Next:** [02-frontend](02-frontend.md) · [07-enterprise](07-enterprise.md) · [frontend 40](../frontend/40-react-native-android-ios/README.md)
