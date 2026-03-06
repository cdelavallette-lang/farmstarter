# Website Link Testing

This directory contains automated tests to verify all links on the Santa Puala Farm website are working correctly.

## Test Script

`test_website_links.py` - Validates all internal links on the website

### What It Tests

✅ **Internal HTML Links** - Verifies all links between pages work correctly  
✅ **CSS/Assets** - Checks that stylesheets and resources exist  
✅ **Document Links** - Validates links to markdown files in grants/, forms/, outreach/  
✅ **Special Protocols** - Correctly handles mailto:, tel:, and other special links  
✅ **External Links** - Lists external links for reference (doesn't validate them)

### How to Run

```bash
cd /opt/FarmGrowth
python3 test_website_links.py
```

### Test Results

The script will show:
- ✅ **Green** - Successful internal links
- ❌ **Red** - Broken links that need fixing
- ⚠️ **Yellow** - External links (informational only)

### Latest Test Results (March 6, 2026)

```
✓ Valid internal links: 40
✗ Broken links: 0
ℹ External links: 14
```

**Status: ✅ ALL TESTS PASSING**

### Files Validated

- index.html
- grant-documents.html
- finding-buyers-guide.html
- new-project-planner.html
- salad-greens-project.html
- ginger-turmeric-project.html
- cut-flowers-project.html
- soil-health-project.html

### When to Run Tests

- Before deploying to GitHub Pages
- After adding new pages or links
- After restructuring directories
- When updating navigation menus

### CI/CD Integration (Optional)

You can add this to a GitHub Actions workflow:

```yaml
name: Test Links
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Test Website Links
        run: python3 test_website_links.py
```
