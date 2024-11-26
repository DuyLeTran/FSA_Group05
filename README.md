# LMS

## Branch hieutt: Quiz Bank

## Description
This is the branch to control the development of Quiz Bank app.<br>
There is a downloadable item below.

### Download Model
IMPORTANT: There is a part to compare question to question using a pretrained Word2Vec model for Vectorizing sentences for more accurate comparisons.<br>
How it is used: This is applied for Add Question module in the app.<br>
What if there is no model detected: The module still detect for similar questions but not as accurate (with simple machine learning).<br>
How to install:
- Download Google's Word2Vec model (here)[https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?pli=1&resourcekey=0-wjGZdNAUop6WykTtMip30g]
- Put the model to this path: .\quiz_bank\views\modules\
