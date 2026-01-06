# Postman Collection for GFW Pro EAPI

This directory contains a complete Postman collection and environment file for testing the GFW Pro External API without writing code.

## Files

- **`GFW_Pro_EAPI.postman_collection.json`** - Postman collection with all API requests organized into workflows
- **`GFW_Pro_EAPI.postman_environment.json`** - Environment variables for the collection

## How to Import the Collection

### Step 1: Import the Collection

1. Open **Postman** (download from [postman.com](https://www.postman.com/downloads/) if needed)
2. Click the **Import** button in the top left corner
3. Choose one of these methods:
   - **File**: Click "Upload Files" and select `GFW_Pro_EAPI.postman_collection.json`
   - **Folder**: Click "Folder" and select this `postman/` directory (imports both files)
   - **Link**: Copy the file path and use "Paste Raw Text" if importing from a URL
4. Click **Import**

### Step 2: Import the Environment

1. In Postman, click **Environments** in the left sidebar (or press `Cmd/Ctrl + E`)
2. Click the **Import** button
3. Select `GFW_Pro_EAPI.postman_environment.json`
4. Click **Import**

### Step 3: Activate the Environment

1. Look at the top right corner of Postman
2. Click the environment dropdown (it may say "No Environment")
3. Select **"GFW Pro EAPI Environment"**

## ⚠️ IMPORTANT: Configure Postman Settings First

**Before making your first API request**, you must configure two Postman application settings:

### 1. Enable Automatic Redirects

1. Click the **gear icon (⚙️ Settings)** in the top-right corner of Postman
2. Go to the **General** tab
3. Find **"Automatically follow redirects"**
4. Turn it **ON** ✅
5. This approximates curl's `--location` and `--post302` behavior, which is required for some API endpoints

### 2. Set HTTP Version to Auto

1. In the same **Settings → General** page
2. Look for **"HTTP version"**
3. Set it to **"Auto"**
4. This lets Postman negotiate the same HTTP version that the server uses, avoiding version-mismatch issues

**Close the Settings window** (changes are saved automatically).

> ⚠️ **If you skip this step, you may encounter errors when making API requests.** These settings ensure Postman behaves like command-line tools (curl) that our API expects.

---

## Updating Environment Variables

After importing, you should update these variables with your own values:

1. Click **Environments** in the left sidebar
2. Click **"GFW Pro EAPI Environment"**
3. Edit these variables:

| Variable | Description | Update Required |
|----------|-------------|-----------------|
| `baseUrl` | API base URL | Yes - Set to your API endpoint |
| `apiToken` | API authentication token | Yes - Your API key |
| `userEmail` | User email address | Yes - Your email |
| `csvFilePath` | Path to CSV file | Optional - For file uploads |
| `commodity` | Commodity type | Optional - Default: "Cocoa Generic" |
| `analysisType` | Analysis type (FCD, Alerts, GHG) | Optional - Default: "FCD" |

## Troubleshooting

If you're getting errors when making requests:

1. **Verify Postman Settings**: Make sure you've enabled "Automatically follow redirects" and set "HTTP version" to "Auto" (see above)
2. **Check Environment**: Ensure "GFW Pro EAPI Environment" is selected in the top-right dropdown
3. **Verify Credentials**: Double-check that `apiToken`, `baseUrl`, and `userEmail` are set correctly
4. **Check Status Code**: If you get an error, note the status code and response body - this will help diagnose the issue

For more detailed troubleshooting, see the [QuickStart Guide](../QUICKSTART_GUIDE.md).

