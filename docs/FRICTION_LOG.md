# Friction log

Dates are 2026. Severity: Low (annoying), Medium (cost real time), High (blocks or nearly blocks the work).

## 1. Vega Virtual Device does not run on Windows
- **Task:** run the Fire TV / Vega simulator on my Windows PC to test the app.
- **Steps:** read the getting started docs for the Vega SDK and virtual device.
- **Expected:** Windows (or WSL) supported, since most hackathon participants use Windows.
- **Actual:** the docs say Windows and WSL are not supported for the Vega virtual device.
- **Severity:** High
- **Workaround:** used the Android Studio Television emulator (Android 11, API 30), which Amazon's own blog uses for Fire OS 8 testing.
  I asked in the hackathon Q&A and was told it is acceptable for the demo.
- **Suggestion:** state the supported operating systems at the top of the Vega getting started page, and offer a cloud or Windows-friendly simulator.

## 2. Docs disagree about which emulator to use
- **Task:** decide how to test a Fire OS app without a device.
- **Steps:** compared the Fire TV testing pages.
- **Expected:** one clear recommendation.
- **Actual:** one page says to use a real device, another says to use an Android Studio virtual device.
- **Severity:** Medium
- **Workaround:** Android Studio TV virtual device, API 30.
- **Suggestion:** one page that lists which Fire TV models run Fire OS and which run Vega OS, and which test option fits each.

## 3. New AWS account: every Amazon Bedrock quota is 0
- **Task:** call Amazon Nova through the Converse API from Lambda.
- **Steps:** created the Lambda and IAM policy, called Converse, then tried the Bedrock Playground with a one-word prompt.
- **Expected:** the default quota (the Service Quotas page shows an AWS default of 8,000,000 tokens per minute for Nova 2 Lite).
- **Actual:** first `AccessDeniedException: Your account is currently being verified`, later `ThrottlingException: Too many tokens per day`,
  even for the word "hi" in the Playground, in us-east-1 and us-west-2, for Nova and Writer models. Service Quotas shows an applied
  value of 0 for TPM and RPM on every Nova model.
- **Severity:** High
- **Workaround:** the Lambda falls back to keyword matching and scripted answers; Polly still works. I filed quota increase requests
  and an AWS Support case (Oct 20); they were still Pending when I submitted.
- **Suggestion:** give new accounts a small non-zero quota for a few Nova models, or show a clear "your quota is 0, request it here" message in the Playground.

## 4. The error talks about "tokens per day" but Service Quotas only lists per-minute quotas
- **Task:** find the quota behind `Too many tokens per day`.
- **Steps:** Bedrock > Quotas, searched "tokens per day".
- **Expected:** a quota with that name.
- **Actual:** no result. Only "tokens per minute" and "requests per minute" rows exist, all showing 0.
- **Severity:** Medium
- **Workaround:** requested increases on the TPM and RPM rows.
- **Suggestion:** make the error text name the actual quota.

## 5. Only one pending quota request at a time
- **Task:** request increases for TPM and RPM (and later for a second model).
- **Actual:** after the first request, the console says "Quota increase request limit reached" and blocks new requests until the pending one closes.
- **Severity:** Medium
- **Workaround:** waited; used the support case for the rest.
- **Suggestion:** allow several requests for different quotas, or show an estimated review time.

## 6. Transparent WebM avatar clips show a solid background in the emulator WebView
- **Task:** show the avatar over the page background in the Fire OS emulator.
- **Expected:** same result as desktop Chrome (alpha transparency).
- **Actual:** the clips (WebM with alpha) looked correct in Chrome but had an opaque background inside the API 30 emulator's WebView.
- **Severity:** Medium
- **Workaround:** [re-exported the clips on a solid dark background with chroma key applied ,added a dark card behind the avatar which is default chroma key applied as it comes to screen the black background gets transparent, none yet the starting remote animation clip show a dark background in the emulator but are transparent in Chrome.]
- **Suggestion:** document the WebView version and codec support of Fire OS 8, including alpha WebM.

## 7. First Gradle sync fails with a timeout
- **Task:** open the new project in Android Studio.
- **Actual:** `Could not install Gradle distribution ... SocketTimeoutException: Connect timed out`.
- **Severity:** Low
- **Workaround:** Try Again (it worked on the next attempt); the first sync then downloads for several minutes.
- **Suggestion:** mention the large first-time download and the offline Gradle option in the Fire TV Android getting started guide.
