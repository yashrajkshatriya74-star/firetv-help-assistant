# Deploying the "Ask anything" backend

The app sends a typed question to a small AWS Lambda function. Amazon Bedrock decides whether the
question matches one of the recorded tutorials (the app then plays that clip) or needs a new answer;
new answers are spoken with Amazon Polly. If Bedrock is not reachable the function falls back to
keyword matching, so the app keeps working.

```
Fire TV app (WebView)  --POST {"question": "..."}-->  Lambda Function URL
                                                        |-- Amazon Bedrock (Converse API)  -> tutorial id or short answer
                                                        '-- Amazon Polly (neural voice)     -> mp3 for fresh answers
```

Use region **US East (N. Virginia)** for everything below.

## 1. Check Bedrock
Bedrock console > Playgrounds > Chat > pick **Amazon Nova Micro** and send "hi". If it answers, access is fine.
If you use another model, copy its Model ID (or inference profile ID) for step 2.

## 2. Create the function
1. Lambda > Create function > Author from scratch > name `firetv-ask`, runtime Python 3.12 (or newer).
2. Paste `lambda_function.py` into the code editor and press Deploy.
3. Configuration > General configuration > Edit: Timeout 20 seconds, Memory 256 MB.
4. Configuration > Permissions > click the role name > Add permissions > Create inline policy > JSON > paste `iam-policy.json`.
5. Optional environment variables: `MODEL_ID` (default `amazon.nova-micro-v1:0`), `VOICE_EN` (default `Joanna`), `VOICE_HI` (default `Kajal`).
6. Configuration > Function URL > Create: auth type **NONE**. Leave "Configure CORS" off, the code answers CORS itself. Copy the URL.

## 3. Test in the Lambda console
Test tab, event JSON:
```json
{"requestContext":{"http":{"method":"POST"}},"body":"{\"question\":\"my video keeps buffering\"}"}
```
Expected: `"type": "clip", "topic": "buffering"`. A general question such as
"what is the difference between HD and 4K" should return `"type": "answer"` with an `audio` field.
If the result has `"source": "fallback"`, read `bedrock_error` in the response: it names the problem
(model access, wrong model ID, missing permission).

## 4. Connect the app
Put the Function URL in `config.json` as `{ "askUrl": "https://....lambda-url.us-east-1.on.aws/" }`,
upload `config.json` next to `index.html`, and invalidate the CloudFront cache.

## Cost guard
The function reads at most 240 characters and asks for at most 220 output tokens. Add an AWS Budget
(for example 5 USD per month) with an email alert.

## Troubleshooting

| Symptom | Meaning |
|---|---|
| `"source": "fallback"` and `bedrock_error` says `AccessDeniedException ... account is currently being verified` | The AWS account is still being verified for Bedrock. Wait, or contact AWS Support. |
| `ThrottlingException ... Too many tokens per day` (also in the Bedrock Playground) | The account's Bedrock quota is 0. Open Service Quotas > Amazon Bedrock, check the TPM and RPM rows of your model (for example Nova 2 Lite), and request an increase. |
| Answers come only from keywords and recorded clips | Normal while Bedrock is unavailable: the function falls back to keyword matching and a few scripted answers (Polly still speaks them). |
| Model in another region | Set the environment variables `BEDROCK_REGION` (for example `us-west-2`) and `MODEL_ID` (for example `global.amazon.nova-2-lite-v1:0`). Polly keeps using the function's region. |
