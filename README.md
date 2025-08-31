# Download saved instgram videos

Instagram doesn't want you downloading videos to your own device. If a video isn't saved on your own machine it can be deleted at any time

```
usage: main.py [-h] [--directory DIRECTORY]

Download Instagram videos using yt-dlp

options:
  -h, --help            show this help message and exit
  --directory DIRECTORY, -d DIRECTORY
                        Where the videos should be downloaded to (Default savedVideos)
```

## Step 1
Go to `https://www.instagram.com/<your username>/saved/all-posts/`.

## Step 2
Paste this into the console. It keeps a list of all seen video links loaded on the page and as you scroll theres code to only keep the current 20 or so video tiles loaded in the DOM. Therefore it polls the DOM every 200ms looking for new video tiles. You'll then need to scroll down the page as far as you want to save videos from.
```javascript
const seenHrefs = new Set();

function checkForNewLinks() {
    const linkElements = document.querySelectorAll('div > a[role="link"]');

    linkElements.forEach(element => {
        const href = element.getAttribute('href');
        if (href && !seenHrefs.has(href)) {
            seenHrefs.add(href);
        }
    });
}

setInterval(checkForNewLinks, 200);
```

### Step 3
When at the bottom of the page or as far back as you want videos saved from run this in your console. It'll spit out a comma seperated list of links to all saved posts (videos and images)
```javascript
Array.from(seenHrefs).filter((link) => link.startsWith("/p/")).join(",")
```

### Step 4
Paste the list into `links.txt` and run the python script using the arguments above or no arguments.

Made most of this using https://www.phind.com/