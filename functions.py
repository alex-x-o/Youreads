import pandas as pd
import re

def get_channel_stats(youtube, channel_ids):
    
    all_data = []
    
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channel_ids)
        )
    response = request.execute()
    
    for item in response['items']:
        data = {'channelName': item['snippet']['title'],
                'subscribers': item['statistics']['subscriberCount'],
                'views': item['statistics']['viewCount'],
                'totalVideos': item['statistics']['videoCount'],
                'playlistId': item['contentDetails']['relatedPlaylists']['uploads']
        }
        
        all_data.append(data)

    return(pd.DataFrame(all_data))

def get_video_ids(youtube, playlist_id):
    
    video_ids = []
    next_page_token = None
    
    while True:
        request = youtube.playlistItems().list(
            part="snippet, contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')
        if next_page_token is None:
            break

    return video_ids

def get_video_details(youtube, video_ids):

    all_video_info = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()

        for video in response['items']:
            stats_to_keep = {'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'favouriteCount', 'commentCount'],
                             'contentDetails': ['duration', 'definition', 'caption']
                            }

            video_info = {}
            video_info['video_id'] = video['id']

            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            all_video_info.append(video_info)
    
    return pd.DataFrame(all_video_info)

def get_book_related_videos(video_df):
    titles = []
    for i in range(len(video_df)):
        title = video_df.loc[i, 'title']
        if re.search(".*books?.*", title):
            titles.append(title)
            
    return titles

def get_comments_in_videos(youtube, video_ids):
    
    all_comments = []
    
    for video_id in video_ids:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=100,
                order="relevance",
            )
            response = request.execute()

            comments_in_video = [comment['snippet']['topLevelComment']['snippet']['textOriginal'] for comment in response['items'][0:100]]
            comments_in_video_info = {'video_id': video_id, 'comments': comments_in_video}

            all_comments.append(comments_in_video_info)
        except:
            print('Could not get comment for video ' + video_id)
    
    return pd.DataFrame(all_comments)

def get_timestamps(comments_in_video):
    new_comments = []
    for i in range(len(comments_in_video)):
        comment = comments_in_video[i]
        if re.search(".*(timestamps?|[0-9]+\.|[0-9]{1,2}:[0-9]{2}).*", comment, re.I):
            new_comments.append(comment)
                
    return new_comments

def get_timestamp_comments(youtube, video_ids):
    
    all_comments = []
    next_page_token = None
    
    for video_id in video_ids:
        while True:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=100,
                order="relevance",
                pageToken=next_page_token
            )
            response = request.execute()

            comments_in_video = [comment['snippet']['topLevelComment']['snippet']['textOriginal'] for comment in response['items'][0:100]]
            new_comments = get_timestamps(comments_in_video)
            if not new_comments:
                continue
            comments_in_video_info = {'video_id': video_id, 'comments': new_comments}

            all_comments.append(comments_in_video_info)
            
            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                break
    
    return pd.DataFrame(all_comments)

if __name__ == "__main__":
    main()