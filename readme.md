# Project4 -- Network
[![Build Status](https://travis-ci.com/fross123/cs50w_project4.svg?token=63YWzg2eCjLxZNQQiney&branch=master)](https://travis-ci.com/fross123/cs50w_project4)

Live test site can be viewed at: https://socialnetworktesting.herokuapp.com/

## New Post
- users can create a new post by submitting the new post form.
    - The new post form is a rich text editor created using quilljs.
-  Redirect to index which renders all of the posts.

## All Posts
- All posts are rendered on the index.html page.

## Profile Page
- Displays current followers, and how many users the displayed user follows.
- All posts from that user are rendered
- Follow or unfollow button is displayed for all users except self.

## Following
- All posts that the current user follows are displayed
- If user is not authenticated, a 404 error is displayed.
    - user would have to type in route manually.

## Pagination
- only 10 posts are displayed at a time.

## Edit Post
- edit post button is displayed if current user is the user of a post.
- textarea is displayed with the text pre-filled with current post content.
- on save, the post is sent to the server via fetch call.
- no other user is able to edit another users post because the button is not displayed for posts that the current user did not create.

## Like and Unlike
- Like and unlike buttons are displayed for posts that users did not create.
- Likes are updated with fetch and the display is updated with javascript.
