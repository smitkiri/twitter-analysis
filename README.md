# twitter-analysis

This web application analyzes a user's twitter account and displays various visualizations. It is made using tweepy api, plotly, flask and implementeed on heroku.

### Installing all dependencies

Installing tweepy, the twitter api for python.\
`pip install tweepy`

Installing plotly, a powerful visualization tool.\
`pip install plotly`

Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and [Heroku](https://devcenter.heroku.com/articles/heroku-cli).

You also need to create a [Twitter Developer account](https://developer.twitter.com/) and get consumer key and access token.

### Getting data using tweepy

The `tweepy.API.user_timeline()` function returns the last 20 tweets of a user. To get more tweets, we need to use the `tweepy.Cursor()` function.

The `user_timeline()` function returns a list of Status objects. The Status object contains a json element which has all the data related to the particular tweet. 

For this application, we will use the `text`, `source`, `created_at`, `lang`, `retweeted`, `is_quote_status` and `in_reply_to_screen_name` attributes of the status object. 

### Using visualizations

This application uses `plotly` to visualize the data gethered from the twitter api.
We need to convert the plotly graph to json and use the `Plotly` javascript to display the visualizations in the html file.

### Deploying on heroku

To deploy the application on heroku, we need to create a free heroku account first.
A useful tutorial to get started wih heroku can be found [here.](https://devcenter.heroku.com/articles/getting-started-with-python)

Once, heroku is set up and all the files needed to deply the app on heroku are ready, use the following commands to deply the app.

`> heroku create`\
`> git push heroku master`\
`> heroku ps:scale web=1`\
`> herou open`

### Useful links

[Tweepy](https://tweepy.readthedocs.io/en/v3.5.0/getting_started.html)

[Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

[Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)

[Plotly for python](https://plot.ly/python/)
