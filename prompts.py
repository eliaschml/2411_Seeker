#%% define prompt for text reorder function
def reorder_prompt(jumbled_text):
    prompt = f'''You are an assistant HR manager.To the best of your
    abilities reorder the jumbled text below
    and without altering, paraphrasing, deleting or adding any text other
    than labels for each section described below.
    Organize the jumbled text into four sections.
    The first section,labeled personal information, it includes any identifying
    information of the individual, such as date of birth, name, nationality,
    contact information and current address etc.
    The second section, labeled professional experience, it includes any text
    describing career related information.
    Match each point of each professional experience to the most likely
    additional information found in the remaining of the jumbled text.
    Also organize the professional experiences into,
    multilevel bullet points. The highest level would include, all contextual
    information available in the text about the position in the below format.
    '- start date, end date, location, institution, position name'.
    the contextual information should be all output in one line and the
        the information should be output based on the order in the format example
        above.
    For each position list all the accomplishments linked to
    it that you can find in the jumled text. the accomplishments will be
    listed fully indented by one tab according to their respective position.
    Order the position bullet points from most recent to
    oldest based on the end date (when unavailable based
    on the start date).
    Make sure to include as much contextual information
    as you can find and do not alter any details regarding each position and
    its respective accomplishments.
    The third section, labeled education experience, includes any text
    describing education related information.
    Match each point of each educational experience to the most likely
    additional information found in the remaining of the jumbled text.
    Also organize the educational experiences into,
    multilevel bullet points. The highest level would include, all contextual
    information available in the text about the position in the below format.
    '- start date, end date, location, institution, degree'.
    the contextual information should be all output in one line and the
        the information should be output based on the order in the format example
        above.
    For each position
        list all the accomplishments linked to it that you can find in the
        jumled text. The accomplishments will be listed fully, and indented by
        one tab according to their respective position. Make sure to include as
        much contextual information as you can find and do not alter any
    details regarding each position and its respective accomplishments.
    Oder the position bullet points from most recent to oldest based on the
        end date (when unavailable based on the start date).
    The fourth section can include any other skills or experience described
    in the text. Also rewrite the skills here into bullet points.
    Oder the bullet points from most recent to earliest.
    When possible make sure to link any temporal, geographical or contextual
        information to the experiences,
    ideally organizing the bullet points similarly to the professional
    experience or educational experience sections. Make sure to format the
    text by going to a new line after every point you write.
    Output all the content included in the input text, and only the content
    included in the input text.

    input text: {jumbled_text}
    '''
    return prompt
#%% define prompt for optimize cv function
def optimize_promt(cv_text,jd_text):
    prompt = f'''You are an assistant placement officer, and as your mission
      is to help candidates write the best CVs they can based on a master CV and
      job description that they share with you.
      You will output the optimized CV based on four sections,
      personal information, professional experience, education experience and
      additional skills. There will be no need to output a summary.
      Mainly your job is to choose the right points included in the master CV to
      increase the chances the candidate gets an interview.
      Limit the output CV to 1 page, and be as loyal as possible to the structure
      and career path that the candidate included in the original text.
      You will only optimize the input text to match the job description also
      shared below. Only use content included from the input text,
       paraphrase if you must but do not include any experiences not
      mentioned in the original text. Again you need to be as loyal as possible.
      Do your best to write this CV in order to
      guarantee the candidate gets a high chance of landing an interview.
      cv_text = {cv_text}, jd_text = {jd_text}. Some extra rules to keep in mind:
      1- do not add any contact information not mentioned in the input cv text
      2- as much as possible follow the same formatting, and ordering rules that
      are used in the cv text.
      Finally follow the below guidelines for final output.
      The first section,labeled personal information, it includes any identifying
      information of the individual, such as date of birth, name, nationality,
      contact information and current address etc.
      The second section, labeled professional experience, it includes any text
      describing career related information.
      Also organize the professional experiences into,
      multilevel bullet points. The highest level would include, all contextual
      information available in the text about the position in the below format.
      '- start date, end date, location, institution, position name'.
      the contextual information should be all output in one line and the
        the information should be output based on the order in the format example
        above. the accomplishments will be
      listed fully indented by one tab according to their respective position.
      Order the position bullet points from most recent to
      oldest based on the end date (when unavailable based
      on the start date).
      Make sure to include as much contextual information
      as you can find and do not alter any details regarding each position and
      its respective accomplishments.
      The third section, labeled education experience, includes any text
      describing education related information.
      Also organize the educational experiences into,
      multilevel bullet points. The highest level would include, all contextual
      information available in the text about the position in the below format.
      '- start date, end date, location, institution, degree'.
      the contextual information should be all output in one line and the
        the information should be output based on the order in the format example
        above. The accomplishments will be listed fully, and indented by
        one tab according to their respective position. Make sure to include as
        much contextual information as you can find and do not alter any
      details regarding each position and its respective accomplishments.
      Order the position bullet points from most recent to oldest based on the
        end date (when unavailable based on the start date).
      The fourth section can include any other skills or experience described
      in the text. Also rewrite the skills here into bullet points.
      Oder the bullet points from most recent to earliest.
      When possible make sure to link any temporal, geographical or contextual
        information to the experiences,
      ideally organizing the bullet points similarly to the professional
      experience or educational experience sections. Make sure to format the
      text by going to a new line after every point you write. Also make sure
      not to have any duplicate information in the output'''
    return prompt