# Consensus

Economic policy is often black-boxed. Our web app, Consensus, aims to streamline the communication, evaluation and discussion of economic policy by connecting citizens, politicians and economists on one platform. Politicians can post their policy proposals, which appear on the feeds of all users. Users can upvote or downvote these posts, politicians and economists can endorse them, economists can give their analysis, and citizens can ask questions. Our data playground feature enhances analysis by using machine learning models such as Logistic Regression and Deep Neural Networks to predict a policy's effect on unemployment and inequality.

## Instructions to run

In order to run this project, first clone this repo to your machine. Then, using the .env.template file, create a .env file, changing the MYSQL_ROOT_PASSWORD to some password you would like to use. Lastly, with docker desktop open, build the docker image by entering "docker compose up -d" in the terminal.