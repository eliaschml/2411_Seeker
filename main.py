from fasthtml import common as fh
import contents
import functions
import os
import json
import datetime as dt
import pytz

UPLOAD_FOLDER = './temp_uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(UPLOAD_FOLDER)

app,rt = fh.fast_app(
    live=True
    ,hdrs=(fh.Link(rel="icon", type='assets/x-icon', href=r'.\assets\favicon-32x32.png'),)
    )
@rt('/learn_more')
def get(): return contents.intro

@rt('/getting_started')

def get(): 
    # div = fh.Div(session['test'])
    return contents.getting_started

@rt('/cv_optimizer')
def get(session):
    if session['record_id']:
        return contents.optimize_cv_loaded
    else:  
        return contents.optimize_cv_upload

@rt('/')
def get(session):
    # create session variables
    session.setdefault('record_id','')
    session.setdefault('jd_id','')
    return contents.title

@rt('/upload_cv')
# uploads pds and extracts raw text
async def post(myFile:fh.UploadFile, session):
    file = await myFile.read()  # Access the file uploaded
    # check file is pdf, and single file
    if myFile and myFile.filename.endswith('.pdf'):
        temp_file_path = os.path.join(UPLOAD_FOLDER
                                    , f'temp_{myFile.filename}')
        # save uploaded file temporarily
        with open(temp_file_path, 'wb') as f:
            f.write(file) # save file
        # extract raw text from pdf    
        jumbled_text = functions.extract_text(temp_file_path)
        # reorder jumbled text using gemini
        reordered_text = functions.reorder_text(jumbled_text) 
        # generate seeker record_id
        record_id = functions.gen_record_id()
        # store record_id to session
        session['record_id'] = record_id
        # create seeker content json file 
        record_content = json.dumps(
            {
            "record_id": record_id
            ,"record_content": reordered_text
            }
        )
        # store seeker file in db
        functions.add_record(record_id,record_content)
        # clear temp uploaded file
        os.remove(temp_file_path)
        upload_status = fh.Details(
                            fh.Summary('CV information analysis complete!✅')
                            ,fh.Div(fh.Code(reordered_text))
                            ,hx_swap="beforeend"
                            ,hx_target='#upload_form_div'
                            )
        #script to enable download button upon upload
        download_button_enabler = fh.Html(
        fh.Script(
            """
            document.getElementById('download_button').disabled = false;
            """,
            hx_swap="attr"
            )
        )
        return upload_status,download_button_enabler
    else:
        return fh.Response('Invalid File format. Please upload a PDF.'
                           ,status=400)

@rt('/download_seeker_file')
# uploads pdfs and extracts raw text
async def get(session):
    # get seeker file
    seeker_file = functions.get_record_dict(record_id=session['record_id'])
    json_string = json.dumps(seeker_file)
    # swap seeker file upload button with record loaded message
    '''seeker_upload_button_disabler = fh.Html(
        fh.Script(
            """
            document.getElementById('submit_seeker_button').disabled = true;
            document.getElementById('seekerFile').disabled = true;
            """,
            hx_swap="attr"
            )
        )'''
    return fh.Html(
        fh.A(f"Download JSON", href=f"data:application/json;charset=utf-8,{json_string}", download="data.json")
    )

@rt('/upload_seeker')
# uploads seeker file and extracts master cv content
async def post(seekerFile:fh.UploadFile, session):
    file = await seekerFile.read()  # Access the file uploaded
    # check file is json, and single file
    session['record_id']=""
    if seekerFile and seekerFile.filename.endswith('.json'):
        temp_file_path = os.path.join(UPLOAD_FOLDER
                                    , f'temp_{seekerFile.filename}')
        # temporarily save seeker file
        with open(temp_file_path, 'wb') as f:
            f.write(file)
        # extract seeker content
        with open(temp_file_path, 'r') as f:
            seeker_content = json.load(f)
        # extract seeker record_id and write to session
        target_record_id = json.loads(seeker_content[0]['record_dict'])['record_id']
        session['record_id']=target_record_id
        # retrieve content from db
        target_master_cv = json.loads(seeker_content[0]['record_dict'])['record_content']
        # clear uploaded seeker file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        # checks if uploaded record id actually matches any record
        if target_master_cv:
            return fh.Div(
                fh.P(
                    f'Record succesfully loaded.'
                )
            )
        else:
            session['record_id'] = seeker_content['record_id']
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            return fh.Div(
                fh.P(
                    '''Couldn't find record, try re-uploading Seeker file.
                        If error persists, try recreating your Seeker file.
                    '''
                )
            )
    else:
        return fh.Response('Invalid File format. Please upload the .json seeker file.'
                        ,status=400)
@rt('/upload_jd')
async def post(jd: contents.Job_Description,session):
    # N.B: target elements are selected in form setup using hx-target 
    if jd.jd_text:
        now = dt.datetime.now(tz=pytz.timezone('UTC'))
        # timestamp excludes tz information and saves now in UTC
        formatted_timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f") + now.astimezone().strftime("%z")
        jd.jd_submit_timestamp = formatted_timestamp
        # create job id, maybe "record_id__job_id" where job_id is time + random numbers
        jd_id = functions.gen_jd_id(session['record_id'])
        jd.jd_id = jd_id
        session['jd_id'] = jd.jd_id
        # store job description in DB
        functions.add_jd(
            session['record_id']
            ,jd.jd_id
            , jd.jd_text
            , jd.jd_submit_timestamp
            )
        # tailor CV and return output
        submission_confirm = fh.P('CV Optimization complete.')
        retrieved_record = functions.get_record_dict(record_id=session['record_id'])[0]
        retrieved_dict = json.loads(retrieved_record['record_dict'])
        record_content = retrieved_dict['record_content']
        optimized_cv = functions.optimize_cv(
            record_content
            ,jd.jd_text
            )
        optimized_cv_div = fh.Div(
            fh.Pre(
                optimized_cv
            )
        )
        return submission_confirm, optimized_cv_div
    else:
        return fh.P(
            'Please enter valid text into the JD field.'
            , hx_swap = 'innerHTML'
            )
# create @rt('/loading') and a loading routing function in contents 
# enabling me to have a loading graphic when BE stuff is happening
fh.serve()