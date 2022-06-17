# SoundLib: A Music Recording Library

SoundLib (abbreviation of sound library), provides a site for users to upload their own music recordings.

## Project Introduction

### Wechat Authentication

Scan QR Code:

https://developers.weixin.qq.com/doc/oplatform/Website_App/WeChat_Login/Wechat_Login.html

Mobile Wechat Authenticate:

https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html

### Upload Recordings

Django supports upload files, so this is not a big deal.

### Searching

Django also supports advanced searching, considering similar vocabulary, weighted words and so on:

https://docs.djangoproject.com/en/4.0/topics/db/search/

## User Guide

### Login

SoundLib only provides signup and login via WeChat service. Laptop users need to scan a QR code using WeChat on a mobile phone to authenticate. Mobile phone users can authenticate in a pop-up window.

### Browse Recordings

Soundlib provides 3 different views.

- Time Line: this view lists recordings on a timeline in ascending order of upload time.
- Members: in this view, recordings are grouped by their uploader, a filter can be further adapted to find a specific user.
- Composers: recordings can also be classified by copmosers of the piece.

### Upload Recordings

When an authenticated user want to upload a new recording, he or she can choose the "upload" tab and include required information in the form.

### Manage Recordings

To be determined.