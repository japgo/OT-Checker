
from datetime import datetime
import login_info
import func

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from pytz import timezone

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

local_test = False

def logging( text:str ):
	print( f'{datetime.now( timezone( "Asia/Seoul" ) )} {text}' )

def run_Approval():
	try:
		if local_test :
			options = webdriver.ChromeOptions()
			# options.add_argument('--headless')
			options.add_argument("--disable-gpu")
			options.add_argument("--no-sandbox")
			driver = webdriver.Chrome( './chromedriver.exe', options=options )
			url = login_info.get_url()
			driver.get( url )

		else:
			chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', "chromedriver")
			options = webdriver.ChromeOptions()
			options.binary_location = chrome_bin
			options.add_argument('--headless')
			options.add_argument("--disable-gpu")
			options.add_argument("--no-sandbox")
			driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
			url = login_info.get_url()
			driver.get( url )





		# login page start
		print( 'login page url : ' + driver.current_url )
		driver.find_element_by_id( 'txtPC_LoginID' ).send_keys( login_info.get_id() )
		driver.find_element_by_id( 'txtPC_LoginPWTemp' ).click()
		driver.find_element_by_id( 'txtPC_LoginPW' ).send_keys( login_info.get_pw() )
		driver.find_element_by_class_name( 'txt_btn_bs' ).click()
		# login page end


		
		try: # 비밀번호 다음에 변경하기.
			WebDriverWait( driver, 10 ).until( EC.visibility_of_any_elements_located( ( By.ID, 'popup_ok' ) ) )
			WebDriverWait( driver, 5 ).until( EC.element_to_be_clickable( ( By.CLASS_NAME, 'txt_btn_bs' ) ) ).click()
   
			WebDriverWait( driver, 10 ).until( EC.visibility_of_any_elements_located( ( By.ID, 'nextChangeBtn' ) ) )
			nextChangeBtn = driver.find_element( by=By.ID, value="nextChangeBtn")
			nextChangeBtn.find_element_by_class_name( 'txt_btn2_bs' ).click()
		except Exception as ex:
			logging( repr( ex ) )
   

		
		try: # 간헐적으로 생성되는 팝업 처리.
			WebDriverWait( driver, 10 ).until( EC.visibility_of_any_elements_located( ( By.ID, 'divPortalBoardPopUP0_p' ) ) )
			logging( 'popup exist!!' )
			WebDriverWait( driver, 5 ).until( EC.element_to_be_clickable( ( By.ID, 'divPortalBoardPopUP0_px' ) ) ).click()
		except Exception as ex:
			logging( repr( ex ) )



		# main page start
		logging( 'main page url : ' + driver.current_url )

		divHeader = driver.find_element_by_css_selector("div[id='divHeader']")

		WebDriverWait( divHeader, 10 ).until( EC.element_to_be_clickable( ( By.ID, 'top_Approval' ) ) ).click()

		# top_Approval = divHeader.find_element( by=By.ID, value="top_Approval" )
		# actions = webdriver.ActionChains( driver )
		# actions.move_to_element( top_Approval ).perform()
		# actions.click().perform()





		logging( '결재 url : ' + driver.current_url )
		WebDriverWait( driver, 10 ).until( EC.visibility_of_any_elements_located( ( By.CLASS_NAME, 'applist2_rt' ) ) )
		WebDriverWait( driver, 10 ).until( EC.presence_of_element_located( ( By.CLASS_NAME, 'approval_btop' ) ) )
		approval_btop = driver.find_element( by=By.CLASS_NAME, value="approval_btop")
		inputSearch = approval_btop.find_element( by=By.ID, value="inputSearch")
		#inputSearch = WebDriverWait( applist2_rt, 20 ).until( EC.element_to_be_clickable( ( By.ID, 'inputSearch' ) ) ) 
		time.sleep( 1 )
		inputSearch.send_keys( '연장' )
		time.sleep( 1 )
		#driver.find_element_by_class_name( 'btn_search_l' ).click()
		WebDriverWait( driver, 10 ).until( EC.visibility_of_element_located( ( By.CLASS_NAME, 'btn_search_l' ) ) ).click()
		time.sleep( 1 )
		WebDriverWait( driver, 10 ).until( EC.visibility_of_element_located( ( By.CLASS_NAME, 'text02_L' ) ) ).click()
		time.sleep( 1 )
		# main page end




		# 연장근무 신청서 window start
		logging( '연장근무 신청서 window start' )
		WebDriverWait( driver, 10 ).until( EC.number_of_windows_to_be( 2 ) )
		driver.switch_to.window( driver.window_handles[ -1 ] )
		ot_window_handle = driver.current_window_handle
		logging( '연장근무 신청서 url : ' + driver.current_url )

		WebDriverWait( driver, 5 ).until( EC.visibility_of_element_located( ( By.ID, 'DivPop_ElectronicApprovalRule_px' ) ) ).click()

		btLine = driver.find_element_by_css_selector("span[id='btLine']")
		btLine.find_element_by_class_name('btn_bs_l').click() # 결재선 선택 버튼 클릭

		# 연장근무 신청서 window end




		# 결재선 window start
		logging( '결재선 window start' )
		WebDriverWait( driver, 10 ).until( EC.number_of_windows_to_be( 3 ) )
		driver.switch_to.window( driver.window_handles[ -1 ] )
		logging( '결재선 url + ' + driver.current_url )

		WebDriverWait( driver, 10 ).until( EC.presence_of_element_located( ( By.NAME, 'rdoApvListGroup' ) ) ).click() #미리 저장된 연장근무 라디오 버튼
		driver.find_element_by_class_name( 'txt_btn2_bs' ).click() #적용 버튼

		driver.find_element_by_id( 'chkDeptTreeEDSoftware3Team__2' ).click() #3팀
		driver.find_element_by_id( 'chkDeptTreeSW1G3T1P__0' ).click()  #1파트
		driver.find_element_by_id( 'chkDeptTreeSW1G3T2P__1' ).click() #2파트

		tblDraftRefAfter = driver.find_element_by_css_selector("div[id='tblDraftRefAfter']")
		tblDraftRefAfter.find_element_by_class_name( 'btn_ws_l' ).click() #참조 버튼


		pop_btn8 = driver.find_element_by_css_selector("table[class='pop_btn8']")
		pop_btn8.find_element_by_class_name( 'btn_bs2_l' ).click() # 결재선 확인 버튼
		# 결재선 window end


		#SW1그룹 3팀 평일 및 휴일 연장근무신청서(10/7)
		driver.switch_to.window( ot_window_handle )
		logging( '연장근무 신청서 url : ' + driver.current_url )
		driver.find_element_by_id( 'SUBJECT' ).send_keys( 'SW1그룹 3팀 평일 및 휴일 연장근무신청서' )

		w_con06_box = driver.find_element_by_css_selector("div[class='w_con06_box']")
		w_con06_box.find_element_by_class_name( 'btn_iws_l' ).click() # 파일 추가 버튼


		DivPop_FileUpload_if = driver.find_element_by_css_selector( "iframe[id='DivPop_FileUpload_if']" )

		driver.switch_to.frame( DivPop_FileUpload_if )
		type_file = driver.find_element_by_css_selector("input[type='file']")

		#file_path = './' + func.get_toady_file_name()
		file_path = os.getcwd() + '/' + func.get_toady_file_name()
		#file_path = os.getcwd() + '\\휴일 및 평일 연장 근무신청서_SW1그룹 3팀.xlsx'
		logging( '파일 경로 : ' + file_path )
		
		file_exist = os.path.isfile( file_path )
		if file_exist is not True :
			logging( f'{file_path} 파일 없음' )
			return False, file_path + ' 파일이 존재 하지 않습니다.'

		type_file.send_keys( file_path ) # 파일 추가.
		logging( '파일 추가 완료.' )

		logging( '파일 업로드 시작.' )
		pop_body2 = driver.find_element_by_css_selector("div[class='pop_body2']")
		pop_body2.find_element_by_class_name( 'btn_bs2_l' ).click() # 확인 버튼 -> 파일 업로드 진행
		#time.sleep( 3 )
		
		driver.switch_to.window( ot_window_handle )
		ly_btn = WebDriverWait( driver, 20 ).until( EC.presence_of_element_located( ( By.CLASS_NAME, 'ly_btn' ) ) )
		ly_btn.find_element_by_class_name( 'btn_bs_l' ).click() # 업로드 확인 알림 창 닫기.
		logging( '파일 업로드 완료.' )

		time.sleep( 1 )
		btDraft = driver.find_element_by_css_selector("span[id='btDraft']")
		btn_bs_l = WebDriverWait( btDraft, 20 ).until( EC.visibility_of_element_located( ( By.CLASS_NAME, 'btn_bs_l' ) ) )
		#btn_bs_l = btDraft.find_element_by_class_name('btn_bs_l')
		btn_bs_l.click() # 기안 버튼 클릭!!!

		#time.sleep( 1 )
		#의견 입력 팝업
		
		# print( 'page0' )
		# driver.switch_to.window( driver.window_handles[ 0 ] )
		# print( driver.page_source )

		# print( 'page1' )
		# driver.switch_to.window( driver.window_handles[ 1 ] )
		# print( driver.page_source )

		logging( '의견 입력 팝업 시작.' )
		WebDriverWait( driver, 10 ).until(EC.number_of_windows_to_be( 3 ) )
		driver.switch_to.window( driver.window_handles[-1] )
		logging( '의견 입력 팝업 열림 확인' )

		pop_btn2 = WebDriverWait( driver, 20 ).until( EC.presence_of_element_located( ( By.CLASS_NAME, 'pop_btn2' ) ) )
		pop_btn2.find_element_by_class_name('btn_bs2_l').click() # 확인 버튼 클릭!!!
		#pop_btn2.find_element_by_class_name('btn_ws2_l').click() # 닫기 버튼 클릭!!!
		logging( '의견 입력 팝업 종료.' )

	
		for handle in driver.window_handles :
			driver.switch_to.window( handle )
			driver.close

		return True, "결재 진행 완료 하였습니다."
	except Exception as error:
		logging( repr(error) )
		return False, "결재 진행 중 오류가 발생 하였습니다."

if local_test :
	run_Approval()