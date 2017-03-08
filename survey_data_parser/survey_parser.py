import csv
import re

filenames = ['PGPTraitandDiseaseSurvey2012-Blood.csv',
             'PGPTraitandDiseaseSurvey2012-Cancers.csv',
             'PGPTraitandDiseaseSurvey2012-CirculatorySystem.csv',
             'PGPTraitandDiseaseSurvey2012-CongenitalTraitsAndAnomalies.csv',
             'PGPTraitandDiseaseSurvey2012-DigestiveSystem.csv',
             'PGPTraitandDiseaseSurvey2012-Endocrine,Metabolic,Nutritional,AndImmunity.csv',
             'PGPTraitandDiseaseSurvey2012-GenitourinarySystems.csv',
             'PGPTraitandDiseaseSurvey2012-MusculoskeletalSystemAndConnectiveTissue.csv',
             'PGPTraitandDiseaseSurvey2012-NervousSystem.csv',
             'PGPTraitandDiseaseSurvey2012-RespiratorySystem.csv',
             'PGPTraitandDiseaseSurvey2012-SkinAndSubcutaneousTissue.csv',
             'PGPTraitandDiseaseSurvey2012-VisionAndHearing.csv']

blood_header = ('Participant', 'Iron deficiency anemia', 'Pernicious anemia (a.k.a. \"AddisonBiermer anemia\")',
                'Folate deficiency anemia', 'Hereditary spherocytosis', 'G6PD deficiency', 'Sickle cell trait (carrier)',
                'Sickle cell anemia', 'Autoimmune hemolytic anemia', 'Hemophilia', 'Von Willebrand disease',
                'Idiopathic thrombocytopenic purpura (ITP)', 'Hereditary thrombophilia (includes Factor V Leiden and Prothrombin G20210A)',
                'Other thrombophilia (includes antiphospholipid syndrome)')

cancer_header = ('Participant', 'Stomach cancer', 'Colon cancer', 'Rectal cancer', 'Colon polyps', 'Pancreatic cancer', 'Lung cancer',
                 'Melanoma', 'Non-melanoma skin cancer', 'Lipoma', 'Breast cancer', 'Breast fibroadenoma', 'Cervical cancer',
                 'Endometrial cancer', 'Uterine fibroids', 'Ovarian cancer', 'Prostate cancer', 'Bladder cancer',
                 'Kidney cancer', 'Thyroid cancer', 'Non-Hodgkin lymphoma', 'Leukemia', 'Polycythemia vera',
                 'Essential thrombocythemia', 'Neurofibromatosis', 'Brain cancer')

circulatory_header = ('Participant', 'Hypertension', 'Myocardial infarction (heart attack)', 'Angina', 'Pulmonary embolism',
                      'Mitral valve prolapse', 'Hypertrophic cardiomyopathy', 'Dilated cardiomyopathy',
                      'Restrictive cardiomyopathy', 'Other cardiomyopathy (including ARVD)', 'Bundle branch block',
                      'Wolff-Parkinson-White (WPW) Syndrome', 'Long QT Syndrome', 'Heart block', 'Atrial fibrillation',
                      'Premature ventricular contractions', 'Sick sinus syndrome (includes tachy-brady syndrome)',
                      'Cardiac arrhythmia', 'Congestive heart failure', 'Stroke', 'Aortic aneurysm',
                      'Other aneurysm', 'Raynaud\'s phenomenon', 'Kawasaki disease',
                      'Hereditary hemorrhagic telangiectasia (also known as Osler-Weber-Rendu syndrome)',
                      'Deep vein thrombosis (DVT)', 'Varicose veins', 'Hemorrhoids', 'Varicocele')

congenital_header = ('Participant', 'Spina bifida', 'Congenital ocular coloboma', 'Congenital heart defect', 'Cleft palate',
                     'Cleft uvula', 'Cleft lip', 'Tongue tie (ankyloglossia)', 'Bifid tongue (cleft tongue)',
                     'Infantile pyloric stenosis', 'Hirschsprung\'s disease', 'Hypospadias', 'Renal agenesis (missing kidney)',
                     'Polycystic kidney disease', 'Congenital hydronephrosis', 'Developmental dysplasia of the hip',
                     'Congenital clubfoot (equinovarus)', 'Polydactyly', 'Syndactyly (webbing of digits)', 'Ehlers-Danlos syndrome',
                     'Congenital ichthyosis', 'Single transverse palmar crease (simian crease)', 'Marfan syndrome')

digestive_header = ('Participant', 'Impacted tooth', 'Dental cavities', 'Gingivitis', 'Temporomandibular joint (TMJ) disorder',
                    'Canker sores (oral ulcers)', 'Geographic tongue', 'Fissured tongue', 'Gastroesophageal reflux disease (GERD)',
                    'Barrett\'s esophagus', 'Peptic ulcer (stomach or duodenum)', 'Appendicitis', 'Inguinal hernia',
                    'Hiatal hernia', 'Crohn\'s disease', 'Ulcerative colitis', 'Diverticulosis', 'Irritable bowel syndrome (IBS)',
                    'Rectal prolapse', 'Acute liver failure', 'Chronic liver disease and cirrhosis',
                    'Nonalcoholic fatty liver disease (NAFLD)', 'Gallstones', 'Celiac disease')

endocrine_header = ('Participant', 'Thyroid nodule(s)', 'Graves\' disease', 'Hypothyroidism', 'Hashimoto\'s thyroiditis',
                    'Diabetes mellitus, type 1', 'Diabetes mellitus, type 2', 'Primary hyperparathyroidism',
                    'Growth hormone deficiency', 'Polycystic ovary syndrome (PCOS)', 'Lactose intolerance',
                    'High cholesterol (hypercholesterolemia)', 'High triglycerides (hypertriglyceridemia)',
                    'Alpha 1-antitrypsin deficiency', 'Gout', 'Hemochromatosis', 'Cystic fibrosis', 'Porphyria', 'Gilbert syndrome')

genitourinary_header = ('Participant', 'Kidney stones', 'Acute kidney failure', 'Chronic kidney failure', 'Urinary tract infection (UTI)',
                        'Urethral diverticulum', 'Benign prostatic hypertrophy (BPH)', 'Male infertility', 'Peyronie\'s disease',
                        'Spermatocele', 'Fibrocystic breast disease', 'Bartholin\'s cyst', 'Endometriosis', 'Uterine prolapse',
                        'Ovarian cysts', 'Female infertility')

musculoskeletal_header = ('Participant', 'Lupus', 'Sjogren\'s syndrome (Sicca syndrome)', 'Rheumatoid arthritis', 'Osteoarthritis',
                          'Chondromalacia patella (CMP)', 'Spinal stenosis', 'Sciatica', 'Frozen shoulder', 'Rotator cuff tear',
                          'Tennis elbow', 'Achilles tendonitis', 'Bone spurs', 'Trigger finger', 'Bunions', 'Dupuytren\'s contracture',
                          'Plantar fasciitis', 'Fibromyalgia', 'Scheuermann\'s kyphosis', 'Osgood-Schlatter disease',
                          'Osteoporosis', 'Flatfeet', 'Postural kyphosis', 'Scoliosis')

nervous_header = ('Participant', 'Recurrent sleep paralysis', 'Parkinson\'s disease', 'Essential tremor', 'Huntington\'s disease',
                  'Restless legs syndrome', 'Spinal muscular atrophy', 'Amyotrophic lateral sclerosis (ALS)', 'Cluster headaches',
                  'Chronic tension headaches (15+ days per month, at least 6 months)', 'Multiple sclerosis (MS)',
                  'Cerebral palsy', 'Epilepsy', 'Migraine with aura', 'Migraine without aura', 'Narcolepsy', 'Arnold-Chiari malformation',
                  'Trigeminal neuralgia', 'Bell\'s palsy', 'Carpal tunnel syndrome',
                  'Hereditary motor and sensory neuropathy (includes Charcot-Marie-Tooth disease and HNPP)',
                  'Other peripheral neuropathy', 'Muscular dystrophy')

respiratory_header = ('Participant', 'Deviated septum', 'Nasal polyps', 'Chronic sinusitis', 'Chronic tonsillitis', 'Allergic rhinitis',
                  'Chronic bronchitis', 'Emphysema', 'Asthma', 'Chronic Obstructive Pulmonary Disease (COPD)')

skin_header = ('Participant', 'Pilonidal cyst', 'Dandruff', 'Eczema', 'Allergic contact dermatitis', 'Rosacea', 'Psoriasis', 'Lichen planus',
               'Keloids', 'Skin tags', 'Hair loss (includes female and male pattern baldness)', 'Alopecia areata',
               'Hyperhidrosis (excessive sweating)', 'Hidradenitis suppurativa', 'Acne', 'Dermatographia', 'Cafe au lait spots')

vision_and_hearing_header = ('Participant','Retinal Detachment','Diabetic retinopathy','Hypertensize retinopathy',
                        'Central serous retinopathy','Age-related macular degeneration', 'Retinits pigmentosa',
                        'Glaucoma','Infantile , juvenilee, and presenile cataract','Age-related cataract',
                        'Traumatic cataract','Hyperopia (Farsightedness)','Myopia (Nearsightedness)',
                        'Astigmatism','Presbyopia','Color blindness','Keratoconus','Dry eye syndrome',
                        'Strabismus','Floaters','Cogential nystagmus','Menieres disease','Otosclerosis',
                        'Age-related hearing loss','Tinnitus','Sensorineural hearing loss or cogential deafness')

header = ''

for filename in filenames:
    if ('Blood' in filename):
        header = blood_header
        print("using Blood file")
        print(header)
        print("\n")
    if ('Cancers' in filename):
        header = cancer_header
        print("using Cancers file")
        print(header)
        print("\n")
    if ('Circulatory' in filename):
        header = circulatory_header
        print("using Circulatory file")
        print(header)
        print("\n")
    if ('Congenital' in filename):
        header = congenital_header
        print("using Congenital file")
        print(header)
        print("\n")
    if ('Digestive' in filename):
        header = digestive_header
        print("using Digestive file")
        print(header)
        print("\n")
    if ('Endocrine' in filename):
        header = endocrine_header
        print("using Endocrine file")
        print(header)
        print("\n")
    if ('Genitourinary' in filename):
        header = genitourinary_header
        print("using Genitourinary file")
        print(header)
        print("\n")
    if ('Musculoskeletal' in filename):
        header = musculoskeletal_header
        print("using Musculoskeletal file")
        print(header)
        print("\n")
    if ('Nervous' in filename):
        header = nervous_header
        print("using Nervous file")
        print(header)
        print("\n")
    if ('Respiratory' in filename):
        header = respiratory_header
        print("using Respiratory file")
        print(header)
        print("\n")
    if ('Skin' in filename):
        header = skin_header
        print("using Skin file")
        print(header)
        print("\n")
    if ('Vision' in filename):
        header = vision_and_hearing_header
        print("using Vision file")
        print(header)
        print("\n")

    out_list = []

    out_list.append(header)

    #lists to insert data into DF

    with open('survey_files/cut_files/'+filename) as csvFile:
        parseFile = csv.reader(csvFile,delimiter=',')
        file_row_count = 0
        for row in parseFile:
            if "Participant" in row:
                continue
            else:
                output_row = []
                i=0
                while i <= len(header):
                    output_row.insert(i,'0')
                    i+=1
                #print(row)
                for item in row:
                    #print("item is: {}".format(item.strip()))
                    if (re.findall(r"hu(\d+)", item) or re.findall(r"hu[A-Z]", item)):
                       output_row[0] = item
                    else:
                        if item.strip() in header:
                            #print("found item {}".format(item))
                            index = header.index(item.strip())
                            #print('index is: {}'.format(index))
                            output_row[index] = '1'
                #print(output_row)
                out_list.append(output_row)

    #print(out_list)

    with open('output/'+filename.replace('.csv','')+'_output.csv', 'w') as csvFile:
        wr = csv.writer(csvFile, dialect='excel')
        for row in out_list:
            wr.writerow(row)