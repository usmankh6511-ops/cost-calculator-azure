# Cost Calculator API — Azure Functions (Serverless)

**Project 4: The Serverless Logic** — DecodeLabs Cloud Computing Internship (Azure Track), Batch 2026

## 📂 Files
```
cost-calculator-azure/
├── function_app.py       # Main Azure Function (HTTP trigger)
├── host.json             # Function app config
├── requirements.txt      # Python deps (azure-functions)
├── local.settings.json   # Local runtime settings (not pushed to Azure)
├── test_events/          # Sample JSON payloads
└── README.md
```

Logic: reads `num1` + `num2` from the request body → returns `{"Sum": total}`.
Already tested locally, output confirmed correct.

---

## 🛠️ Step 0 — Install tools (one-time)

```bash
# Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Azure Functions Core Tools
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

## 🔑 Step 1 — Login to Azure

```bash
az login
```
This opens a browser link — login with your DecodeLabs/Azure sandbox account.
📸 **Screenshot yahan lena:** terminal jo dikhaye "Login successful" ya subscription list.

## 🏗️ Step 2 — Create Resource Group + Storage + Function App

```bash
# Variables — apne naam se replace kar lena (globally unique naam chahiye storage/functionapp ke liye)
RESOURCE_GROUP="decodelabs-project4-rg"
LOCATION="eastus"
STORAGE_NAME="costcalcstorage$RANDOM"
FUNCTION_APP="cost-calculator-$RANDOM"

# Resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Storage account (Functions needs this)
az storage account create --name $STORAGE_NAME \
  --resource-group $RESOURCE_GROUP --location $LOCATION \
  --sku Standard_LRS

# Function App (Python, Consumption/serverless plan = pay-per-execution)
az functionapp create --resource-group $RESOURCE_GROUP \
  --consumption-plan-location $LOCATION \
  --runtime python --runtime-version 3.11 \
  --functions-version 4 \
  --name $FUNCTION_APP \
  --storage-account $STORAGE_NAME \
  --os-type Linux
```
📸 **Screenshot yahan lena:** Azure Portal → Resource groups → apna `decodelabs-project4-rg` khol ke resources ki list (storage account + function app dono dikhne chahiye).

## 🚀 Step 3 — Deploy the code

```bash
cd cost-calculator-azure
func azure functionapp publish $FUNCTION_APP
```
Ye command deploy khatam hone par ek URL dega jaise:
```
https://cost-calculator-xxxx.azurewebsites.net/api/costcalculator
```
📸 **Screenshot yahan lena:** terminal ka "Deployment successful" output (jisme function URL bhi dikhe).

## 🧪 Step 4 — Test the deployed function

```bash
curl -X POST "https://<your-function-app>.azurewebsites.net/api/costcalculator" \
  -H "Content-Type: application/json" \
  -d '{"num1": 7, "num2": 3}'
```
Expected: `{"Sum": 10}`

Doosra test:
```bash
curl -X POST "https://<your-function-app>.azurewebsites.net/api/costcalculator" \
  -H "Content-Type: application/json" \
  -d @test_events/test_2.json
```
Expected: `{"Sum": 40}`

📸 **Screenshot yahan lena:** terminal jisme curl ka request + `{"Sum": ...}` response dono dikhein
(ya Postman use kar rahe ho to Postman ka response screenshot).

**Portal se bhi test kar sakte ho** (console likhne ki zaroorat nahi):
1. Azure Portal → Function App → apna function → **Code + Test** tab
2. **Test/Run** click karo → Body mein `{"num1": 7, "num2": 3}` daalo → **Run**
3. Output panel mein `{"Sum": 10}` dikhega
📸 **Screenshot yahan lena:** yehi Test/Run wala output panel.

## 📊 Step 5 — Check logs (proof of execution + billing)

```bash
func azure functionapp logstream $FUNCTION_APP
```
Ya Portal se:
Function App → **Monitor** tab → **Logs** (Application Insights) → recent invocations.
📸 **Screenshot yahan lena:** Monitor/Logs tab jisme execution duration aur success status dikhe
(ye tumhara "millisecond billing, zero idle cost" ka proof hai).

---

## 🐙 Step 6 — Push to GitHub

```bash
cd cost-calculator-azure
git init
git add .
git commit -m "Project 4: Serverless Cost Calculator API (Azure Functions)"
git branch -M main
git remote add origin https://github.com/<your-username>/cost-calculator-azure.git
git push -u origin main
```
Phir GitHub par repo ko **Public** kar dena:
Repo → **Settings** → **General** → **Danger Zone** → **Change visibility** → **Public**
📸 **Screenshot yahan lena:** GitHub repo ka page (public badge dikhna chahiye) + folder structure.

---

## 📤 Submission Checklist

- [x] Code working properly (locally verified: `{"Sum": 10}` ✅)
- [x] Project files complete
- [ ] GitHub repo created & Public — Step 6
- [x] README added (this file)
- [ ] Screenshots — 5 jagah marked upar (📸 wale)
- [x] Final project tested (curl / Postman / Portal Test tab)

## 🧹 Step 7 — Cleanup (optional, taake sandbox credits na lagein)
```bash
az group delete --name $RESOURCE_GROUP --yes --no-wait
```
(Sirf submission/screenshots complete karne ke baad chalana — resource group delete karne se function app bhi chala jayega.)

---
*Tools: Azure Functions (Consumption Plan) | Language: Python 3.11 | DecodeLabs — Batch 2026*
