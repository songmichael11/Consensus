# Consensus

Economic policy is often black-boxed. Our web app, Consensus, aims to streamline the communication, evaluation and discussion of economic policy by connecting citizens, politicians and economists on one platform. Politicians can post their policy proposals, which appear on the feeds of all users. Users can upvote or downvote these posts, politicians and economists can endorse them, economists can give their analysis, and citizens can ask questions. Our data playground feature enhances analysis by using machine learning models such as Logistic Regression and Deep Neural Networks to predict a policy's effect on unemployment and inequality.

## Instructions to run

In order to run this project, first clone this repo to your machine. Then, using the .env.template file in the api folder, create a .env file, changing the MYSQL_ROOT_PASSWORD to some password you would like to use. Lastly, with docker desktop open, build the docker image by entering "docker compose up -d" in the terminal. With the docker containers running, you can then access the web app by going to http://localhost:8501 in a web browser.

## Instructions to use

Upon going to localhost:8501, you will be taken to our landing page, where you can log in as different citizens, politicians, and economists. Once you log in, you will see a feed of mock-posts from different mock-politicians. Users can upvote, downvote and save posts, and politicians can endorse the posts of fellow politicians. By clicking "see more" on a post, you can see the graph associated with a post, the description, as well as sections for expert opinions and voter questions. Economists can add to the expert opinions section, and voters can ask questions that economists and politicians can answer. Users can also explore the data in the given proposal by opening them in the data playground, which allows users to produce graphs with different data and view a variable's effects on unemployment and inequality. Users may also save graphs to access them later.

## Project blog

Throughout the journey of building this MVP, we have kept a blog that contains status updates on our team progress, as well as individual blog posts containing details about our individual contributions and general life updates in our study-abroad journey.

[Click here to visit our amazing blog](https://smpollak.github.io/MPSS-25su-DoC-Blog/)

## Individual contributions

### Sean Blundin
<to be written>

### Paulo Martinez-Amezaga
At the beginning, I assisted same with the first ML Model. I also fetched, cleaned, merged, and stored the data from the Worldbank and some OECD data. My biggest contribution was building the Deep Neural Network. I built a Deep Neural Network to predict GINI and was able to obtain a better r^2. Then I built a Deep Neural Network to predict Unemployment. I built residual plots, obtained r^2 scores and used K fold cross validation in order to ensure our DNN model was in a good enough spot to deploy. I then worked with Sean to deploy the Deep Neural Network into our final product.

### Sam Pollak
At the beginning, I conceptualized our first ML model, then fetched, cleaned, merged and stored most of the data from APIs, including 14 different features from 2 different sources. Then, I built our linear and logistic regression models from numpy and evaluated them using residual plots, r^2 scores and cross-validation tests. I then helped make refinements to our data playground to make it feel more intuitive to the user, including descriptions for each feature, formatting each number input with minimums, maximums, steps and default values, working with Sean to implement presets using real data, and automatic adjusting of the min and max values on the graph to reflect a reasonable range. I also implemented the feature to open a graph from a post or the saved graphs page into the data playground

### Michael Song
<to be written>