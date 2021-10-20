# sqlalchemy-challenge
Using SQLALchemy and Flask to explore Climate data and present it.

- Initial commit was just uploading the necessary files and creating the resources folder.

For the climate_start activity:
- First pass through I was able to mostly complete the Measurement & Precipitation analysis as well as the graph for the most active station.
- Struggled to find use the functions to find the minimum, average, and maximum temperature data from the most active station so I did it 2 ways.
  - I was happy with both results, one actually used the query func. methods and the other I pulled the data and used a list comprehension to make a separate iterable list.

For the Flask/API construction activity:
- Had a huge struggle actually figuring out how to have it request the specific data and organize it into a dictionary that I could jsonify.
- Once I figured it out using my notes, the rest of the problems followed the same format.
- Had another struggle understanding the syntax to make the start and end date api work.
  - I'm only pretty sure I got it working.

Tried to start bonus.
- Struggled to filter data once I got the dates as the index.
- Will continue to work on this in my freetime.
