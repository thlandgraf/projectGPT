
# Project Implementation Guidelines
This document serves as a roadmap outlining our project's structure, the grouping of components, and their interaction. Adherence to these guidelines will ensure a well-organized, maintainable codebase that aligns with our project's objectives and architectural design.

# we want to use the component "app" as the component for the main window
## for the infoboxes on the main page we want to use a separate, reuseable component "infobox"
Here is an example of the usage of the infobox component:
```html
<app-infobox>
    <h1>Header of infobox</h1>
    <p>Your content goes here<p> 
</app-infobox>
```
## for the carousel on the mainpage we want this to be implemented with the component "carousel", which comes with ngx-bootstrap 
Here is an example of the usage of the infobox component:
```html
<app-carousel content="carouselObjects"></app-carousel>
```
where the carouselObjects are defined in the using component als follows:
```jsx
carouselObjects = [ {text="text1", image="/assets/image1.png"}, {text="text2", image="/assets/image2.png"} ]
``` 
## For the navbar we want to use a separate component called "navbar"
The navbar component shall show a 32x32 logo on the left hand side and a language chooser on the right hand side. The Language chooser shall be
implemented with the bootstrap dropdown component. 
## For the footer we want to use a separate component called "footer" 
The footer component shall yield a copyrigt remark and a linkt to the imprint page
# We want to have a component "imprint" for another page impront