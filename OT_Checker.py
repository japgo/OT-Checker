

import slack_token

test = False
BOT_ID, BOT_TOKEN, CHANNEL_NAME = slack_token.get_bot_id_and_token_and_channel( test )
APP_LEVEL_TOKEN = slack_token.get_app_level_token()


import slack_sdk
import time
from datetime import datetime, timedelta
from pytz import timezone
import func
import web_control

bot = slack_sdk.web.client.WebClient( token = BOT_TOKEN )
resp = bot.conversations_list()
# print( "conversations_list : ", resp )


channel_list = resp[ 'channels' ]
for channel in channel_list :
	# print( "channel : ", channel )
	if channel[ 'name' ] == CHANNEL_NAME :
		ch_info = channel

# print( "general info : ", ch_general_info )
ch_id = ch_info[ 'id' ]

# bot.chat_postMessage( channel=ch_id, text = "Check Start!" )


print( 'start!' )
while True :
	now = datetime.now( timezone( 'Asia/Seoul' ) )
	yesterday = now - timedelta(days=1)
	yesterday_str = '{}-{}-{} 00:00:00'.format( yesterday.year, yesterday.month, yesterday.day )
	yesterday_timestamp = time.mktime( datetime.strptime( yesterday_str, "%Y-%m-%d %H:%M:%S" ).timetuple() )
	
	today_timestamp = time.mktime( now.timetuple() )

	time.sleep( 2 )

	#print( "=================================================" )
	try:
		resp = bot.conversations_history( channel = ch_id, lastest = today_timestamp, oldest = yesterday_timestamp )
	except:
		time.sleep( 10 )
		print( "conversations_history exception" )
		continue

	conversation_history = resp[ "messages" ]
	#print( conversation_history )

	checked = False
	for msg in conversation_history:
		text = str( msg[ "text" ] )
		msg_ts = msg[ "ts" ]


		if BOT_ID == msg[ "user" ]:
			continue

		if text.count( "오늘" ) >= 1 and text.count( "야근" ) >= 1 and text.count( "명단" ) >= 1 :
			reaction_required = False
			reaction_list = msg.get( "reactions" )
			
			if reaction_list == None:
				reaction_required = True
			else:
				for reaction_item in reaction_list:
					if BOT_ID not in reaction_item[ "users" ]:
						reaction_required = True


			if reaction_required:
				bot.reactions_add( channel = ch_id, name = "white_check_mark", timestamp = msg_ts )
				ret_str = "야근 인원이 있나요?"
				try:
					if text.count( "상신" ) >= 1 or text.count( "결재" ) >= 1 or text.count( "기안" ) >= 1:
						bot.chat_postMessage( channel=ch_id, text="결재 진행 중 입니다. 잠시만 기다려 주세요." )
						success, ret_str = web_control.run_Approval()
						bot.chat_postMessage( channel=ch_id, text=ret_str )

					else:
						today_file_name = func.get_toady_file_name()
						res = bot.files_upload( channels=CHANNEL_NAME, file=today_file_name, filetype='xlsx' )
						print( res )
				except:
					bot.chat_postMessage( channel=ch_id, text=ret_str )

		try:
			if BOT_ID in msg[ "reply_users" ]:
				checked = True

		except:
			checked = False
		
		slash_cnt = text.count( '/' )
		if( slash_cnt != 2 ):
			continue
  
		if checked == False:
			reply = ""
			success, err = func.parsing_text( text )
			if success:
				reply = func.get_reply()
			else:
				reply = "잘못된 야근 신청 입니다.. q(≧▽≦q) " + err

			bot.chat_postMessage( channel = ch_id, thread_ts = msg_ts, text = reply )


	#print( "=================================================" )
	#break
	