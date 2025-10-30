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



