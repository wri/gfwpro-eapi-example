# GFW Pro API QuickStart Guide: Testing with Postman

## Welcome! 👋

This guide will help you test the GFW Pro External API using Postman in just a few minutes. By the end, you'll have successfully uploaded location data and retrieved forest analysis results—giving you a clear understanding of what the API can do for your organization.

**What you'll accomplish:**
- ✅ Set up Postman with our pre-configured API collection
- ✅ Configure Postman settings for optimal API compatibility
- ✅ Upload location coordinates (latitude/longitude)
- ✅ Request forest analysis for your locations
- ✅ Download and view analysis results

**Time required:** 15-20 minutes

**Prerequisites:** 
- Postman installed ([download here](https://www.postman.com/downloads/) if needed)
- API credentials (provided by your GFW Pro representative)
- Basic familiarity with Postman (opening requests and clicking "Send")

---

## Overview

The GFW Pro API helps you analyze forest conditions and risks for specific locations. The workflow is straightforward:

1. **Prepare** → Get a secure upload URL
2. **Upload** → Send your location data (CSV file for example)
3. **Create List** → Register your locations and request analysis
4. **Check Status** → Monitor analysis progress
5. **Download** → Get your results

Don't worry—we've pre-configured everything in Postman so you can focus on testing the API, not setting up complex requests.

---

## Step 1: Setup

### 1.1 Download Postman Collection

1. Visit our [GitHub repository](https://github.com/wri/gfwpro-eapi-example)
2. Navigate to the `postman/` folder
3. Download these two files:
   - `GFW_Pro_EAPI.postman_collection.json`
   - `GFW_Pro_EAPI.postman_environment.json`

> 💡 **Tip:** You can also download the entire repository as a ZIP file and extract just the `postman` folder.

### 1.2 Import into Postman

1. **Open Postman** (download from [postman.com](https://www.postman.com/downloads/) if needed)

2. **Import the Collection:**
   - Click the **Import** button (top left)
   - Click **Upload Files**
   - Select `GFW_Pro_EAPI.postman_collection.json`
   - Click **Import**

   > 📸 *Screenshot placeholder: Postman Import screen showing the collection file selected*

3. **Import the Environment:**
   - Click **Environments** in the left sidebar (or press `Cmd/Ctrl + E`)
   - Click **Import**
   - Select `GFW_Pro_EAPI.postman_environment.json`
   - Click **Import**

4. **Activate the Environment:**
   - Look at the top right corner of Postman
   - Click the environment dropdown (it may say "No Environment")
   - Select **"GFW Pro EAPI Environment"**

   > 📸 *Screenshot placeholder: Environment dropdown showing "GFW Pro EAPI Environment" selected*

### 1.3 Configure Postman Settings

**⚠️ IMPORTANT:** Before making your first API request, you must configure two Postman settings:

1. **Enable Automatic Redirects:**
   - Click the **gear icon (⚙️ Settings)** in the top-right corner of Postman
   - Go to the **General** tab
   - Find **"Automatically follow redirects"**
   - Turn it **ON** ✅
   - This approximates curl's `--location` and `--post302` behavior, which is required for some API endpoints

2. **Set HTTP Version to Auto:**
   - In the same **Settings → General** page
   - Look for **"HTTP version"**
   - Set it to **"Auto"**
   - This lets Postman negotiate the same HTTP version that the server uses, avoiding version-mismatch issues

3. **Close the Settings window** (changes are saved automatically)

> ⚠️ **If you skip this step, you may encounter errors when making API requests.** These settings ensure Postman behaves like command-line tools (curl) that our API expects.

> 📸 *Screenshot placeholder: Postman Settings → General tab showing "Automatically follow redirects" ON and "HTTP version" set to "Auto"*

### 1.4 Get Your API Credentials

You should have received:
- **API Token** (a long string like `ILW3l9Dkuc5Y5YiqXm67S8nIOdOJZYch8mAi8BKN`)
- **Base URL** (usually `https://pro.globalforestwatch.org/api/v1` or a QA/staging URL)
- **Your Email Address** (used for tracking and notifications)

> ⚠️ **Don't have credentials?** Contact your GFW Pro representative or support team.

### 1.5 Configure Environment Variables

1. Click **Environments** in the left sidebar
2. Click **"GFW Pro EAPI Environment"** to edit it
3. Update these three required variables:

   | Variable | Value | Example |
   |----------|-------|---------|
   | `apiToken` | Your API token | `ILW3l9Dkuc5Y5YiqXm67S8nIOdOJZYch8mAi8BKN` |
   | `baseUrl` | API base URL | `https://pro.globalforestwatch.org/api/v1` |
   | `userEmail` | Your email | `your.name@company.com` |

4. Click **Save** (important!)

   > 📸 *Screenshot placeholder: Environment variables screen showing the three required variables filled in*

---

## Step 2: Making Your First Request

Now let's walk through the complete workflow. We'll use the **"1. Upload and List Flow"** folder in Postman, which contains all the requests in the correct order.

### 2.1 Prepare Upload

This step gets a secure URL where you'll upload your location data.

1. In Postman, expand **"1. Upload and List Flow"** folder
2. Click on **"Prepare Upload"**
3. Look at the request details:
   - **Method:** POST
   - **URL:** `{{baseUrl}}/prepare_upload` (automatically uses your environment variable)
   - **Headers:** Includes `x-api-key` header (automatically uses your `apiToken`)
   - **Body:** Contains `userEmail` and `fileType: "csv"`

4. Click the **Send** button (top right)

**What to expect:**
- **Status:** `200 OK` or `302 Found` (both are success!)
- **Response:** JSON with `uploadId` and `uploadUrl`

**Example Response:**
```json
{
  "uploadId": "abc123-def456-ghi789",
  "uploadUrl": "https://s3.amazonaws.com/bucket/signed-url-here"
}
```

> ✅ **Success Indicator:** You see `uploadId` and `uploadUrl` in the response

> 📸 *Screenshot placeholder: Postman showing successful Prepare Upload response with uploadId and uploadUrl highlighted*

**What happened?** Postman automatically saved the `uploadId` and `uploadUrl` to your environment variables. You don't need to copy them—they'll be used automatically in the next step!

**Understanding the Response:**
- `uploadId`: Unique identifier for your upload (used in the next step)
- `uploadUrl`: Secure, temporary URL where you'll upload your file (expires after a few minutes)

---

### 2.2 Upload File

Now you'll upload a CSV file with your location coordinates.

**First, prepare your CSV file:**

Create a file called `locations.csv` with this content (or use our sample file from the repository):

```csv
Location Name,Latitude,Longitude,Analysis Radius,Analysis Area,Company,Contact
Farm A,-8.933,-52.138,0.5,,My Company,John Doe
Farm B,5.834,-5.323,0.5,,My Company,Jane Smith
```

**Required columns:**
- `Location Name` - A name for this location (text)
- `Latitude` - Latitude coordinate (-90 to 90, decimal number)
- `Longitude` - Longitude coordinate (-180 to 180, decimal number)
- `Analysis Radius` - Radius in kilometers (e.g., `0.5` for 500 meters, must be a number)

**Optional columns:** `Analysis Area`, `Company`, `Contact` (can be left empty)

**Now upload the file:**

1. Click on **"Upload File"** request in Postman
2. Go to the **Body** tab
3. Select **"binary"** mode (or "file" if available)
4. Click **Select Files** or **Choose Files**
5. Choose your `locations.csv` file
6. Click **Send**

**What to expect:**
- **Status:** `200 OK`
- **Response:** Usually empty or a success message

> ✅ **Success Indicator:** Status code 200 with no error message

> 📸 *Screenshot placeholder: Postman Body tab showing binary file selection with locations.csv selected*

**Understanding the Request:**
- **Method:** PUT (used for uploading files)
- **URL:** Uses the `{{uploadUrl}}` from the previous step automatically
- **Headers:** Includes `Content-Type: text/csv`
- **Body:** Your CSV file content

---

### 2.3 Create List

This step registers your uploaded locations and requests forest analysis.

1. Click on **"Create List"** request
2. Look at the **Body** tab - it's already configured! The request includes:
   - `uploadId` - Automatically filled from Step 2.1
   - `listName` - Auto-generated with timestamp (e.g., `client_demo_1704067200`)
   - `commodity` - Default: "Cocoa Generic" (you can change this in environment variables)
   - `analysisIDs` - Default: "FCD" (Forest Change Detection)

3. Click **Send**

**What to expect:**
- **Status:** `200 OK` or `302 Found`
- **Response:** JSON with `listId`

**Example Response:**
```json
{
  "listId": 12345,
  "uploadId": "abc123-def456-ghi789",
  "status": "Pending"
}
```

> ✅ **Success Indicator:** You see a `listId` in the response

> 📸 *Screenshot placeholder: Postman showing Create List request body with all fields visible, and successful response with listId*

**What happened?** The `listId` was automatically saved. Your analysis has started! This may take a few minutes depending on the number of locations.

**Understanding the Request:**
- `uploadId`: Links to the file you uploaded (automatically filled)
- `listName`: A name for your list (auto-generated, but you can customize)
- `commodity`: Type of commodity (required field, default: "Cocoa Generic")
- `analysisIDs`: Type of analysis to run (options: "FCD", "Alerts", "GHG", "DefReport")

**Understanding the Response:**
- `listId`: Unique identifier for your list (use this to check status)
- `status`: Current status of the list ("Pending" means it's queued for processing)

---

### 2.4 Poll Analysis Status

Check if your analysis is complete.

1. Click on **"Poll Analysis Status"** request
2. Notice the URL includes `{{listId}}` and `{{analysisType}}` - these are automatically filled!
3. Click **Send**

**What to expect:**
- **Status:** `200 OK`
- **Response:** JSON with analysis status

**Example Response (Still Processing):**
```json
{
  "status": "Running",
  "listId": "12345",
  "analysisType": "FCD",
  "progress": 45
}
```

**Example Response (Complete):**
```json
{
  "status": "Completed",
  "listId": "12345",
  "analysisType": "FCD",
  "resultUrl": "https://s3.amazonaws.com/bucket/results.zip",
  "creationDate": "2024-01-15T10:30:00Z",
  "expirationDate": "2024-02-15T10:30:00Z"
}
```

**Status Values:**
- `Pending` - Analysis hasn't started yet
- `Running` - Analysis in progress (wait and check again)
- `Completed` - ✅ Analysis finished successfully!
- `Error` - Something went wrong (see troubleshooting below)
- `Expired` - Results are no longer available (need to regenerate)

> ✅ **Success Indicator:** Status is `Completed` and you see a `resultUrl`

> 📸 *Screenshot placeholder: Postman showing Poll Status response with "Completed" status and resultUrl highlighted*

**If status is "Running":** Wait 30-60 seconds, then click **Send** again. Repeat until status is "Completed".

**Understanding the Response:**
- `status`: Current analysis status
- `resultUrl`: URL to download your results (only present when status is "Completed")
- `creationDate`: When the analysis was created
- `expirationDate`: When the results will expire (download before this date!)

---

### 2.5 Download Results

Get your analysis results!

1. Click on **"Download Results"** request
2. The URL is automatically set to `{{resultUrl}}` from the previous step
3. Click **Send**

**What to expect:**
- **Status:** `200 OK`
- **Response:** A ZIP file download

4. Click **Save Response** → **Save to a file**
5. Save the file (e.g., `my-analysis-results.zip`)

**What's in the ZIP?**
- Analysis reports (PDF or JSON)
- Geospatial data files (GeoJSON, Shapefile, or KML)
- Summary statistics
- Error reports (if any locations had issues)

> ✅ **Success Indicator:** You successfully downloaded a ZIP file

> 📸 *Screenshot placeholder: Postman showing Download Results with "Save Response" option visible*

**Congratulations! 🎉** You've successfully completed the full workflow!

---

## Step 3: Understanding Responses

### Success Responses

**Prepare Upload Response:**
```json
{
  "uploadId": "abc123-def456",
  "uploadUrl": "https://s3.amazonaws.com/..."
}
```
- `uploadId`: Unique identifier for your upload (used in next step)
- `uploadUrl`: Secure URL where you'll upload your file (expires in ~5 minutes)

**Create List Response:**
```json
{
  "listId": 12345,
  "uploadId": "abc123-def456-ghi789",
  "status": "Pending"
}
```
- `listId`: Unique identifier for your list (use this to check status)
- `status`: Current status ("Pending" means queued for processing)

**Status Response (Complete):**
```json
{
  "status": "Completed",
  "listId": "12345",
  "analysisType": "FCD",
  "resultUrl": "https://s3.amazonaws.com/bucket/results.zip",
  "creationDate": "2024-01-15T10:30:00Z",
  "expirationDate": "2024-02-15T10:30:00Z"
}
```
- `status`: Current analysis status
- `resultUrl`: URL to download your results (only when "Completed")
- `analysisType`: Type of analysis performed (FCD, Alerts, GHG, etc.)
- `expirationDate`: Download before this date!

### Common Error Responses

**401 Unauthorized:**
```json
{
  "message": "Unauthorized"
}
```
- **Cause:** Invalid or missing API token
- **Fix:** 
  1. Check your `apiToken` in environment variables
  2. Verify the token is correct (no extra spaces)
  3. Ensure the environment is selected (top-right dropdown)

**400 Bad Request:**
```json
{
  "error": "Validation error",
  "details": "Missing required field: commodity"
}
```
- **Cause:** Missing required field in request body
- **Fix:** Check that all required fields are included:
  - `prepare_upload`: Requires `userEmail` and `fileType`
  - `create_list`: Requires `uploadId`, `listName`, `commodity`, and `analysisIDs`

**404 Not Found:**
```json
{
  "message": "List not found"
}
```
- **Cause:** Invalid `listId` or list doesn't exist
- **Fix:** Verify the `listId` is correct (check from Create List response)

**422 Validation Error (Zod):**
```json
{
  "error": "Validation failed",
  "issues": [
    {
      "path": ["latitude"],
      "message": "Expected number, received string"
    }
  ]
}
```
- **Cause:** Wrong data type (e.g., latitude as text instead of number)
- **Fix:** Check your CSV file - ensure numbers are numeric, not text
  - Latitude/Longitude must be numbers: `-8.933` not `"-8.933"`
  - Analysis Radius must be a number: `0.5` not `"0.5"`

**500 Internal Server Error:**
```json
{
  "message": "Internal server error"
}
```
- **Cause:** Server-side issue
- **Fix:** Wait a few minutes and try again, or contact support with the `listId`

**Analysis Status "Error":**
```json
{
  "status": "Error",
  "errorsDetails": [
    "File is empty",
    "Invalid geometry at location: Farm A"
  ]
}
```
- **Cause:** Issues with uploaded data (invalid coordinates, empty file, etc.)
- **Fix:** 
  1. Check the `errorsDetails` array for specific issues
  2. Verify your CSV file format matches the example
  3. Ensure coordinates are valid (latitude: -90 to 90, longitude: -180 to 180)

---

## Step 4: Next Steps

### Explore Other Endpoints

Now that you've completed the basic workflow, try these other endpoints:

**List Management:**
- **List All Lists** - See all your uploaded lists (paginated)
- **Get List Details** - Get detailed information about a specific list
- **Delete List** - Remove a list (requires `userEmail` in body)

**Other Analysis Types:**
- **Alerts Analysis** - Forest change alerts for date ranges (see "2. Alerts Analysis Flow")
- **GHG Analysis** - Greenhouse gas emissions analysis (see "3. GHG Analysis Flow")
- **DefReport** - Deforestation reporting

All these are pre-configured in the Postman collection—just expand the folders and try them!

### Understanding Analysis Types

- **FCD (Forest Change Detection)**: Identifies forest loss and gain over time
- **Alerts**: Real-time forest change alerts (requires date range: `startDate` and `endDate`)
- **GHG**: Calculates greenhouse gas emissions (requires `yield` data in kg/ha)
- **DefReport**: Generates deforestation reports for compliance

### Tips for Success

1. **Use the Sample Data:** Start with the provided sample CSV (`sample_data/example.csv`) to ensure everything works
2. **Check Status Regularly:** Analysis can take 2-10 minutes depending on number of locations
3. **Save Your listId:** Write down the `listId` from Create List response for reference
4. **Read Error Messages:** Error responses usually explain what's wrong
5. **Start Small:** Test with 2-3 locations first, then scale up
6. **Check Expiration Dates:** Download results before the `expirationDate`

---

## Troubleshooting

### "I can't see the collection after importing"
- **Solution:** Check the **Collections** tab in the left sidebar
- Refresh Postman: `Cmd/Ctrl + R`

### "Variables aren't being filled automatically"
- **Solution:** 
  1. Make sure you selected "GFW Pro EAPI Environment" from the dropdown (top right)
  2. Check that variables are saved (click Save after editing)
  3. Verify variable names match exactly (case-sensitive)

### "401 Unauthorized error"
- **Solution:** 
  1. Go to Environments → "GFW Pro EAPI Environment"
  2. Verify `apiToken` is correct (no extra spaces, no quotes)
  3. Click Save
  4. Try the request again
  5. Check that the environment is selected (top-right dropdown)

### "File upload fails"
- **Solution:**
  1. Make sure CSV file is saved (not just open in Excel)
  2. Use "binary" mode in Postman Body tab
  3. Check file size (should be under 10MB for testing)
  4. Verify the `uploadUrl` hasn't expired (get a new one if needed)

### "Analysis status stays 'Running' forever"
- **Solution:**
  - This is normal for large datasets (can take 10+ minutes)
  - Keep checking every 30-60 seconds
  - If it's been over 15 minutes, check the `listId` is correct
  - Contact support if status is "Running" for more than 30 minutes

### "I get a validation error"
- **Solution:**
  - Check your CSV file format matches the example exactly
  - Ensure column headers are spelled correctly (case-sensitive)
  - Verify latitude/longitude are numbers, not text
  - Check that Analysis Radius is a number (e.g., `0.5`)
  - Ensure no empty required fields

### "Redirect errors or connection issues"
- **Solution:**
  1. Verify Postman settings are configured (see Step 1.3):
     - "Automatically follow redirects" → ON
     - "HTTP version" → Auto
  2. Check Postman Console (View → Show Postman Console) for detailed errors
  3. Try the request again after configuring settings

---

## Additional Resources

- **Full API Documentation:** [GFW Pro API Confluence Space](https://gfw.atlassian.net/wiki/external/MzYyYmY2ZmI1ZTY4NGEzOGJkYTMzZjQzOTQ3MjlkNDU)
- **GitHub Repository:** [gfwpro-eapi-example](https://github.com/wri/gfwpro-eapi-example)
- **Python Examples:** See the `flows/` directory in the GitHub repo for code examples
- **Postman Collection Documentation:** See [`postman/README.md`](postman/README.md) for detailed collection information
- **Support:** Contact your GFW Pro representative or support team

---

## Summary Checklist

By completing this guide, you should have:

- [x] Downloaded and imported the Postman collection and environment
- [x] Configured Postman settings (automatic redirects, HTTP version)
- [x] Set up your API credentials in environment variables
- [x] Successfully prepared an upload
- [x] Uploaded location data (CSV file)
- [x] Created a list and requested analysis
- [x] Checked analysis status
- [x] Downloaded analysis results

**You're now ready to integrate the GFW Pro API into your workflows!** 🚀

---

## Questions?

If you encounter issues not covered here:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review the [Full API Documentation](https://gfw.atlassian.net/wiki/external/MzYyYmY2ZmI1ZTY4NGEzOGJkYTMzZjQzOTQ3MjlkNDU)
3. Check the Postman Console (View → Show Postman Console) for detailed error messages
4. Contact your GFW Pro representative or support team

---

*Last updated: January 2025*

