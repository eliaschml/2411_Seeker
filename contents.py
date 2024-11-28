from fasthtml import common as fh
from dataclasses import dataclass

#%% job description data class defintion
# JD class is assigned jd text and jd id at form submit
@dataclass
class Job_Description:
    jd_text: str = ''
    jd_id: str = ''
    jd_submit_timestamp: float = 0.0
    
# this file contains all contents for the webpage
#%% Intro content
intro = fh.Section(
    fh.Div(
        fh.H2('What is Seeker?')
        ,fh.P('''Seeker is an AI based tool that 
              tailors your CV for each job posting you're applying for''')
    )
    ,fh.Div(
        fh.H3('How it works')
        ,fh.P('''During job searches we’ve all found ourselves writing
               a sort of “master CV”. A CV in which we list all our 
              experience and refer to write a new “tailored CV” for 
              each job app...Seeker is here to help you spend less 
              time doing that!''')
    )
    ,fh.Div(
        fh.H3('Next Steps')
        ,fh.Ol(
            fh.Li('''Upload your “master CV” file in PDF format and 
               receive your Seeker file*''')
            ,fh.Li('''Input your target job posting''')
            ,fh.Li('Get optimized contents for your CV in no time')
        )
    )
    ,fh.Div(
        fh.P(
            '''*you can choose to skip step 1 by uploading your 
            Seeker file (that you made on your first visit)'''
        )
    )
    ,id='main_section'
)
#%% Title
title =  fh.Titled('Seeker'
                   ,fh.H2('Your personal CV optimizer')
                   ,fh.Section(
                        fh.Button("First Time?"
                                , hx_get ="/getting_started"
                                , hx_target = '#main_section'
                                )
                        ,fh.Button("Optimize CV"
                                , hx_get ="/cv_optimizer"
                                , hx_target = '#main_section'
                                )
                            ,fh.Button("What is Seeker?"
                                , hx_get ="/learn_more"
                                , hx_target = '#main_section'
                                )
                            ,style="display: flex; justify-content: space-between"
                            ,id='nav_bar'
                        )
                    ,intro
)
#%% First time
getting_started = fh.Section(
    fh.Div(
        fh.H2('Is your master CV ready?')
        ,fh.P('''Your master CV should include all your Professional 
              Experience, Educational Experience as well as 
              Additional Skills. It’s the information Seeker uses to 
              tailor your CV''')
    )
    ,fh.Div(
        fh.H2('Upload your master CV and analyze its content')
        ,fh.P('''Select and upload your master CV in PDF''')
        ,fh.Form(
            fh.Input(
                    type='file'
                     ,accept='.pdf'
                     ,id='myFile'
                     )
            ,fh.Input(type='submit')
            ,hx_post='/upload_cv'
            ,enctype='multipart/form-data'
        )
        ,id='upload_form_div'
    )
    ,fh.Div(
        fh.H2('Download Seeker file')
        ,fh.Details(
            fh.Summary('Data Disclaimer')
            ,fh.Div(
                fh.P('''By uploading files to Seeker you agree to 
                     Seeker’s data policy below. Seeker is still 
                     prototype. While our priority is to deliver a 
                     way for job seekers to streamline applying to 
                     multiple job posts without being delayed by tedious 
                     tasks like tailoring their CV for every Job 
                     Application. We are saving some of the data input to 
                     study the viability of the product and deduce 
                     interesting insights that would help job seekers in 
                     the future.''')
                ,fh.Br()
                ,fh.B(fh.P('Here is a description of our policy:'))
                ,fh.Ul(
                    fh.Li('We do not save names')
                    ,fh.Li('We do not save contact information')
                    ,fh.Li('''We do not save addresses (we will use your 
                           address/location info to deduct a city or 
                           country but discard any lower 
                           granularity data)''')
                )
            )
            )
        ,fh.P('''Fyi: This may take a few moments''')
        ,fh.Button(
            "Download"
            , hx_get ='/download_seeker_file'
            , disabled=True
            , id = 'download_button'
            )
    )
    ,id='main_section'
)
#%% Seeker file upload section
optimize_cv_common = fh.Section(
    fh.Div(
        fh.H2('Input JD text')
        ,fh.P('Paste the job description you want your CV tailored to', id='jd-form-description')
    )
    ,fh.Div(
        fh.Form(
            fh.Input(type='textarea', id='jd_text')
            ,fh.Input(type='submit')
            ,hx_post='/upload_jd'
            ,hx_target="#output_text"
            ,id='jd_input_form'
        )
    )
    ,fh.Div(
        fh.H2('Your Tailored CV')
        ,fh.P('Tailored CV will be output here', id = 'output_text')
        ,id='output_div'
    )
)
optimize_cv_upload = fh.Section(
    fh.Div(
        fh.H2('Upload Seeker File')
        ,fh.P('Upload required')
        ,fh.Form(
            fh.Input(
                    type='file'
                     ,accept='.json'
                     ,id='seekerFile'
                     )
            ,fh.Input(
                type='submit'
                ,id='submit_seeker_button')
            ,hx_post='/upload_seeker'
            ,enctype='multipart/form-data'
        )
        ,id='seeker_upload_form_div'
    )
    ,optimize_cv_common
    ,id='main_section'

)
#%% Seeker file loaded section
optimize_cv_loaded = fh.Section(
    fh.Div(
        fh.H2('Seeker file loaded')
        ,fh.P('Please proceed to input your desired job description')
    )
    ,optimize_cv_common
    ,id='main_section'
)