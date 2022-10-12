# ff-cal
Forex Factory ICS filter

Filter out low priority items and allow Evolution to import only the good events... cleaning up your calendar. 


### Docker

```
docker build -t ff-cal .
docker run -d -p 8080:8008 ff-cal

# Add a new calendar of type (On The Web) to Evolution pointing at localhost:8080.
```
