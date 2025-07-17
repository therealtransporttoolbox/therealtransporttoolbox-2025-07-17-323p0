# TheRealTransportToolbox Landing Page Maintenance Guide

This guide will help you maintain and customize the TheRealTransportToolbox landing page. Whether you're new to web development or need a quick reference, follow these detailed instructions for common maintenance tasks.

## Table of Contents
1. [Updating Text and Styling](#updating-text-and-styling)
2. [Managing Links](#managing-links)
3. [Adding Privacy and Terms Pages](#adding-privacy-and-terms-pages)
4. [Troubleshooting](#troubleshooting)

## Updating Text and Styling

### Header Section
The header contains the main navigation and logo text. To update:

1. **Logo Text:**
```html
<a href="/" class="text-2xl font-bold bg-gradient-to-r from-purple-500 to-blue-500 bg-clip-text text-transparent">
    TheRealTransportToolbox
</a>
```
- Simply replace "TheRealTransportToolbox" with your desired text
- Keep the classes intact to maintain the gradient effect

### Hero Section
Located at the top of the page, containing the main headline and subtitle:

```html
<h1 class="text-4xl md:text-5xl lg:text-6xl font-bold mb-8 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
    Make safety & compliance easy, stress-free, and profitable.
</h1>
<p class="text-xl md:text-2xl text-gray-300 mb-12">
    Your complete solution for transport compliance and safety management.
</p>
```

**Tailwind CSS Class Explanation:**
- `text-4xl`: Base font size (mobile)
- `md:text-5xl`: Medium screen font size
- `lg:text-6xl`: Large screen font size
- `mb-8`: Bottom margin spacing

### Features Section
Each feature card follows this structure:
```html
<div class="bg-gray-800/50 rounded-2xl p-8 hover:transform hover:scale-105 transition-all duration-300 border border-gray-700 hover:border-purple-500/50">
    <!-- Content -->
</div>
```

To add a new feature card:
1. Copy the entire div structure
2. Paste within the `grid grid-cols-1 md:grid-cols-3 gap-12` container
3. Update the icon, title, and description text

## Managing Links

### Navigation Menu Links
Current navigation links are:
```html
<div class="hidden md:flex space-x-8">
    <a href="#features" class="hover:text-purple-400 transition-colors">Features</a>
    <a href="#benefits" class="hover:text-purple-400 transition-colors">Benefits</a>
    <a href="#faq" class="hover:text-purple-400 transition-colors">FAQ</a>
    <a href="#contact" class="hover:text-purple-400 transition-colors">Contact</a>
</div>
```

To update a link:
1. Locate the `<a>` tag
2. Change the `href` attribute
   - Use `#section-name` for same-page links
   - Use full URLs for external links
3. Update the link text between the tags

### Call-to-Action Links
Located in the hero and CTA sections:
```html
<a href="https://transportcompliancehub.com" class="inline-block px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full">
    Get Started Now
</a>
```
- Replace `https://transportcompliancehub.com` with your desired URL
- Keep the classes to maintain button styling

## Adding Privacy and Terms Pages

### Footer Modification
Add privacy and terms links to the footer:

1. Locate the footer section:
```html
<div class="grid grid-cols-1 md:grid-cols-4 gap-12">
    <div class="space-y-4">
        <!-- Add here -->
    </div>
</div>
```

2. Add the new links:
```html
<div class="space-y-4">
    <h3 class="text-xl font-semibold mb-4">Legal</h3>
    <ul class="space-y-2">
        <li><a href="/privacy.html" class="text-gray-400 hover:text-purple-400 transition-colors">Privacy Policy</a></li>
        <li><a href="/terms.html" class="text-gray-400 hover:text-purple-400 transition-colors">Terms of Service</a></li>
    </ul>
</div>
```

## Troubleshooting

### Common Issues and Solutions

1. **Broken Gradient Text**
If gradient text isn't showing:
- Ensure all these classes are present:
  ```
  bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent
  ```

2. **Responsive Issues**
If mobile layout breaks:
- Check for `md:` prefixed classes
- Verify the container has `mx-auto px-6`

3. **Link Not Working**
For internal links (#section):
- Ensure the section ID matches exactly
- IDs are case-sensitive
- Remove any spaces in IDs

### Need Help?
- Check the Tailwind CSS documentation for class references
- Validate HTML at [W3C Validator](https://validator.w3.org/)
- Test responsive design using browser developer tools

Remember to:
- Always backup before making changes
- Test changes across different devices and browsers
- Keep consistent styling throughout the page
- Maintain the existing color scheme and gradients