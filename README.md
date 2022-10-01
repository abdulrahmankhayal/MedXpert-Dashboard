## The Dashboard:

### The home page:

The main page contains charts related to the progress of current medications and the user's commitment to his medications. On the right, we see the graphs, and on the left an introductory text and a set of buttons that are used to control the charts. At the top there is a button to navigate between the dashboard pages

![Graphical user interface, application Description automatically generated](media/5934f0f4bc75dc7f9c43f51ffa85d58d.jpg)

### Home page charts:

1.  At the top there are set of pie charts, one for each drug. Each chart represents an individual drug, and the ratio within it expresses progress in taking the drug.

![](media/448603f5e1758fd8f9362b9c5a4d9e3a.jpeg)

1.  At the bottom there is a chart showing the user’s commitment to his medications in the last 28 days. The chart consists of a heatmap inside it scatter plots. The heatmap expresses the extent of the user’s commitment to all his medications on a particular day. The more committed the user is, the redder the color in the box representing the day. The scatter is used to express a single drug and its doses, each drug has a unique symbol representing it and a color representing the dose status whether blue if the user takes his dose or gray if he missed it.

### Home page means of interactivity:

The home page contains several means of user interaction.

![](media/13e7af235875bbe3f0ae6be2ca749d48.jpeg)

-   On the left of the page there is a calendar in which user can control the date range for displaying the commitment chart. He can also choose certain medications to display instead of all medications, in addition to a reset button to return the chart to its default appearance.

![Graphical user interface, application Description automatically generated](media/673d4d4ed257c47e4f4de8362a52c8b2.jpeg)

-   At the bottom of the commitment chart there is an interactive legend that user can hide and display the existing drugs by clicking on them.

![](media/b8b9751130c01e6968c53333efeada4f.jpeg)

-   ![](media/f255480592f1878386b1156094861d22.jpeg)When user hovers over a field in the commitment chart, a more informative data that is not present in the chart appears, such as the date and the actual percentage of commitment.
-   in addition to the Plotly toolbar, through which user can save the chart or zoom in and navigate through the chart and many more.

![Graphical user interface, application Description automatically generated](media/2289d8c0f3b3f51c342655cd1427ce7f.jpeg)

### The explore button

The explore button at the top allows the user to navigate between the dashboard pages

![Graphical user interface, application Description automatically generated](media/bca181248e56679734b0e438479aa743.png)

### Measurement page

Same as home page layout, On the right, we see charts, and on the left an introductory text and a set of buttons that are used to control the figure, the page contains a set of line charts describing the change in user vitals over the time.

![](media/3145bb6a258becc31ed847f529483388.jpeg)

### Measurement page charts:

Single figure consist of many virtical subplots each subplot represent a vital.

![Graphical user interface, table Description automatically generated](media/37dc8daeb467dac445b5aefeaf7330e5.png)

### Measurement page means of interactivity:

-   On the left of the page there is a calendar by which the user controls the date range to see measurements within. He can also choose to display information for one or more condition, control which vitals to show insights, in addition to a reset button to return the chart to its default appearance and some useful annotations.

![](media/c4109ce81a61e7f731b2213d72c76c0d.jpeg)

![](media/a37be43639af98277ef108aec406d0c8.jpeg)Show condition annotation:

Coloring regions of the chart for each condition to allow user seeing at which condition these measurements recorded.

![](media/81c54e6cc902044621e3515bca7e9f9b.jpeg)

![](media/015b5b0c3d143ad3e1808c82a9bdecd7.jpeg)Show guidelines annotation:

Show the user information about vital he is looking at, indicating the critical values of vitals and to what extent values are critical

![Graphical user interface, timeline Description automatically generated](media/ace0b62ccbd6d8d2bcc8f20f70aa6c62.jpeg)

-   ![](media/51642ab8fa3a6c92516baf072d67ef7b.jpeg)When the user hovers over a data point in the chart, a more informative data will show off.
-   In addition to the Plotly toolbar.

### Medication timeline page

This page contains insights about user whole medication history, the figure consists of many horizontal bar charts, designed to handle a long timeline full of medication as well as gaps.

Interactivity includes date range selection, selection of drugs, selection of doctors, informative data when hovering and many more.

![Timeline Description automatically generated with low confidence](media/05cd0a19e47a45a5c1cbbdadc3a0452f.png)
