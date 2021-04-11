from django.shortcuts import render, HttpResponse, redirect
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.conf.urls.static import static
from .models import Client, Product, Cont_us, Registered_Users
from AucPage import models
import re, random, string
from datetime import date, datetime
from django.http import JsonResponse
import math
from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
from imutils.video import VideoStream, FPS
import numpy as np
from django.db.models import Max


count=0

def Gen_otp(size):
    gen_pass = ''.join([random.choice( string.ascii_uppercase + string.ascii_lowercase + string.digits) for n in range(size)])
    return gen_pass

def Home(request):
    today = date.today()
    p = Product.objects.all()
    todayAuc=[]
    upcomingAuc=[]
    
    for i in p:
        try:
            already=Registered_Users.objects.get(User_Name=request.user.username,Product_ID=i.id)
        except:
            if request.user.username!=i.Product_owner:
                if i.Auction_pref_date==today:
                    todayAuc.append(i)
                if i.Auction_pref_date>today:
                    upcomingAuc.append(i)
    return render(request, 'Home/Home.html', {'todayAuc':todayAuc, 'upcomingAuc':upcomingAuc})

@login_required(login_url="/Login", redirect_field_name="Home")
def Auc_Page(request):
    return render(request, 'Auction/EnterForm.html')

@login_required(login_url="/Login", redirect_field_name="Home")
def auctionRegister(request, p_id):
    uname_req = request.user.username
    u_obj = Client.objects.get(Uname=uname_req)
    p_obj = Product.objects.get(id=p_id)
    return render(request,'Home/AuctionRegister.html', {'ClientInfo':u_obj, 'ProdInfo':p_obj})

def handleRegisterForm(request):
    if request.method=="POST":
        aucRegUName = request.POST['aucRegUname']
        aucRegEmail = request.POST['aucRegEmail']
        aucRegProdName = request.POST['aucRegProdName']
        aucRegProdDesc = request.POST['aucRegProdDesc']
        aucRegProdOwnerName = request.POST['aucRegProdOwnerName']
        aucRegAucDate = request.POST['aucRegAucDate']
        aucRegAucTime = request.POST['aucRegAucTime']
        client_obj = Client.objects.get(Uname=aucRegUName)
        prod_obj = Product.objects.get(Product_owner=aucRegProdOwnerName, Product_name=aucRegProdName, Product_desc=aucRegProdDesc)
        #Saving in database
        reg_obj = Registered_Users(User_Name= aucRegUName, User_Email= aucRegEmail, Product_Name= aucRegProdName, Product_Owner= aucRegProdOwnerName, Auction_date= prod_obj.Auction_pref_date, Auction_time= prod_obj.Auction_pref_time,PassCode=prod_obj.Auction_Passcode, Product_ID=prod_obj.id, Initial_Bid_Amt=prod_obj.Starting_Bid)
        reg_obj.save()
        messages.success(request, 'Your pre-Registration has been Successfully Done!\nWe have sent you a mail regarding Auction details.')
        subject="AucOn"
        messaging = render_to_string('Home/preRegisterEmail.html',{'Client':client_obj, 'Product':prod_obj})
        from_email=settings.EMAIL_HOST_USER
        email_to_send=EmailMessage(subject=subject, body=messaging, from_email=from_email, to=[client_obj.Email])
        email_to_send.content_subtype = "html"
        email_to_send.send(fail_silently=False)
        return redirect('Home')
    return redirect('Home')

def Login(request):
    return render(request, 'Home/Login.html')

def Signup(request):
    return render(request, 'Home/Signup.html')

def handleSignup(request):
    if request.method == 'POST':
        F_name = request.POST['F_name']
        L_name = request.POST['L_name']
        Uname = request.POST['Signup_Uname']
        DOB = request.POST['DOB']
        Gender = request.POST['gender']
        Aadhar = request.POST['Signup_aadhar']
        Email = request.POST['signup_email']
        Contact = request.POST['contact']
        Address = request.POST['Signup_Address']
        Work_status = request.POST['work_status']
        Work_desc = request.POST['desc_work']
        pwd1 = request.POST['pwd1']
        pwd2 = request.POST['pwd2']
        user_pic=request.FILES['user_pic']
        print(user_pic)
        # Validation:
        if len(Uname)>15:
            messages.error(request, 'Username must be of maximum 15 characters.')
            return redirect('/Signup.html')
        if not Uname.isalnum():
            messages.error(request, 'Username must contain only Letters and Numbers (Alpha-numeric).')
            return redirect('/Signup.html')
        if pwd1 != pwd2:
            messages.error(request, 'Passwords Donot Match.')
            return redirect('/Signup.html')

        myuser=User.objects.create_user(Uname, Email, pwd1)
        myuser.first_name = F_name
        myuser.last_name = L_name
        myuser.Profile_pic = user_pic
        myuser.cont = Contact
        myuser.address = Address
        myuser.aadhar = Aadhar
        myuser.birthdate = DOB
        myuser.gend = Gender
        myuser.workstat = Work_status
        myuser.Work_desc = Work_desc
        myuser.save()
        #client_obj = Client.objects.create_user(Uname, Email, pwd1)
        client_obj = Client(First_name=F_name, Last_name=L_name, Uname=Uname, DOB=DOB, Gender=Gender, Aadhar=Aadhar, Contact=Contact, Email=Email, Address=Address, Work_status=Work_status, Work_desc=Work_desc, password=pwd1)
        client_obj.First_name = F_name
        client_obj.Last_name = L_name
        client_obj.Profile_pic = user_pic
        client_obj.Contact = Contact
        client_obj.Address = Address
        client_obj.Aadhar = Aadhar
        client_obj.DOB = DOB
        client_obj.Gender = Gender
        client_obj.Work_status = Work_status
        client_obj.Work_desc = Work_desc
        client_obj.save()
        messages.success(request, 'Your Account has been Successfully Created!\nWe have sent you a mail.')
        subject="AucOn"
        messaging = render_to_string('Home/Signup_Email.html',{'USER':Uname})
        from_email=settings.EMAIL_HOST_USER
        email_to_send=EmailMessage(subject=subject, body=messaging, from_email=from_email, to=[Email])
        email_to_send.content_subtype = "html"
        email_to_send.send(fail_silently=False)
        return redirect('/Login')
    else:
        messages.error(request, 'Details not provided as required!\nPlease fill the form again.')
        return redirect('/Signup')

def TnC(request):
    messages.info(request, 'Please read carefully!')
    return render(request, 'Home/TermsNcond.html')

def forgotPwd(request):
    return render(request, 'Home/Forgot_pwd.html')

def handleForgotPwd(request):
    if request.method=='POST':
        forgotPwdEmail = request.POST['forgotPwdEmail']
        newPwd = request.POST['newPwd']
        get_client = Client.objects.get(Email=forgotPwdEmail)
        get_client.password = newPwd
        get_client.save()
        get_user = User.objects.get(email=forgotPwdEmail)
        get_user.set_password(newPwd)
        get_user.save()
        messages.success(request, f'Password changed successfull.')
        return redirect('Home') 
    else:
        messages.warning(request, f'Invalid Credentials! Password not changed.')
        return redirect('Home')

def handleLogin(request):
    if request.method == 'POST':
        login_Uname=request.POST['login_Uname']
        login_email = request.POST['login_email']
        login_pwd=request.POST['login_pwd']
        user = authenticate(username=login_Uname, password=login_pwd)
        #user = Client.objects.get(Uname = login_Uname, password = login_pwd)
        #print(user)
        if user is not None:
            login(request, user)
            messages.success(request, f'Logged In Successfull.\nWelcome {login_Uname}.')
            return redirect('Home')
        else:
            messages.error(request, 'Invalid Credentials provided.\nUnable to Login. Please Try again.')
            return redirect('/Login')
    return HttpResponse('404 Not Found')

@login_required(login_url="/Login", redirect_field_name="Home")
def log_out(request):
    logout(request)
    messages.success(request, 'Successfully Logged-Out.')
    return redirect('Home')

@login_required(login_url="/Login", redirect_field_name="Home")
def profile(request):
    uname_req = request.user.username
    u_obj= Client.objects.get(Uname=uname_req)
    p=Product.objects.all()
    #p = Product.objects.get(Product_owner=u_obj.Uname)
    return render(request, 'Home/Profile.html', {'ClientInfo':u_obj, 'ProdInfo':p})

@login_required(login_url="/Login", redirect_field_name="Home")
def sellProduct(request):
    uname_req = request.user.username
    u_obj= Client.objects.get(Uname=uname_req)
    return render(request, 'Home/Sell_item.html', {'ClientInfo':u_obj})

@login_required(login_url="/Login", redirect_field_name="Home")
def handleSellProd(request):
    if request.method == 'POST':
        uname_req = request.user.username
        #user_id = request.user
        #Prod_own=request.POST['prod_owner']
        Prod_name=request.POST['prod_name']
        Prod_buy_date=request.POST['prod_buy_date']
        Start_bid=request.POST['starting_bid']
        Pref_date=request.POST['pref_date']
        Pref_time=request.POST['pref_time']
        Prod_desc=request.POST['prod_desc']
        prod_img = request.FILES['prod_img']
        print(prod_img)
        Prod_passcode = Gen_otp(5)
        prod_obj = Product(Product_owner= uname_req, Product_name= Prod_name, Product_img = prod_img, Product_bought_date= Prod_buy_date, Starting_Bid= Start_bid, Auction_pref_date=Pref_date, Auction_pref_time=Pref_time, Product_desc=Prod_desc, Auction_Passcode=Prod_passcode)
        prod_obj.Product_owner = uname_req
        #prod_obj.Prod_Owner_info = user_id.id
        prod_obj.Product_name = Prod_name
        prod_obj.Product_bought_date = Prod_buy_date
        prod_obj.Starting_Bid = Start_bid
        prod_obj.Auction_pref_date = Pref_date
        prod_obj.Auction_pref_time = Pref_time
        prod_obj.Product_desc = Prod_desc
        prod_obj.Product_img = prod_img
        prod_obj.Auction_Passcode = Prod_passcode
        prod_obj.save()
        messages.success(request, 'Successfully Added Product!')
        return redirect('Home')
    else:
        messages.error(request, 'Details not provided as required!')
        return redirect('Home')


def Contact_Us(request):
    return render(request, 'Home/Contact_Us.html')

def handleContactUs(request):
    if request.method=='POST':
        Full_name = request.POST['Full_name']
        Last_name = request.POST['Last_name']
        email_addr = request.POST['email_addr']
        ph_no = request.POST['ph_no']
        Content = request.POST['Content']
        Contact_us = Cont_us(Full_name=Full_name, Last_name=Last_name, email_addr= email_addr, ph_no=ph_no, Content=Content)
        Contact_us.save()
        #obj1=User.objects.get(email=email_addr)
        #USER=obj1.username
        USER = Full_name + ' ' + Last_name
        subject="AucOn"
        messaging = render_to_string('Home/Email_Cont_us.html',{'USER':USER})
        from_email=settings.EMAIL_HOST_USER
        email_to_send=EmailMessage(subject=subject, body=messaging, from_email=from_email, to=[email_addr])
        email_to_send.content_subtype = "html"
        email_to_send.send(fail_silently=False)
        messages.success(request, 'Response is Recorded.\nA mail regarding this has been sent to you.')
    return render(request, 'Home/Contact_us.html')

def About_Us(request):
    return render(request, 'Home/About_Us.html')


global a
b=True
def facecam_feed(request,p_id):
    try:
        global a
        a=Hand_gesture(p_id,request.user.username)
        return StreamingHttpResponse(gen(a), content_type="multipart/x-mixed-replace;boundary=frame")
    except: 
        pass



def getUsers(request,Product_id):
    
    # queryset=models.Auction.objects.all().order_by('-ClientInitialBid')
    queryset=models.Auction.objects.filter(ProductID=Product_id).order_by('-ClientInitialBid')
    return JsonResponse({'users':list(queryset.values())})



def index(request):
 	return render(request, 'Auction/AucMain.html')

def gen(camera):
    global b
    b=True
    while b:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')




class Hand_gesture():
    def __init__(self,p_id,uname):
        self.vs = VideoStream(src=0).start()
        self.fps = FPS().start()
        self.p_id= p_id
        self.uname=uname

    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        # grab the frame from the threaded video stream
        img = self.vs.read()
        img = cv2.flip(img, 1)

        cv2.rectangle(img, (250, 200), (25, 25), (0, 255, 0), 0)
        crop_img = img[25:200, 25:250]

        # convert to grayscale
        grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # applying gaussian blur
        value = (35, 35)
        blurred = cv2.GaussianBlur(grey, value, 0)

        # thresholdin: Otsu's Binarization method
        _, thresh1 = cv2.threshold(blurred, 127, 255,
                                   cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # show thresholded image


        # check OpenCV version to avoid unpacking error
        (version, _, _) = cv2.__version__.split('.')

        if version == '3':
            image, contours, hierarchy = cv2.findContours(thresh1.copy(), \
                                                          cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        elif version == '4':
            contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, \
                                                   cv2.CHAIN_APPROX_NONE)

        # find contour with max area
        cnt = max(contours, key=lambda x: cv2.contourArea(x))

        # create bounding rectangle around the contour (can skip below two lines)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 0, 255), 0)

        # finding convex hull
        hull = cv2.convexHull(cnt)

        # drawing contours
        drawing = np.zeros(crop_img.shape, np.uint8)
        cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)

        # finding convex hull
        hull = cv2.convexHull(cnt, returnPoints=False)

        # finding convexity defects
        defects = cv2.convexityDefects(cnt, hull)
        count_defects = 0
        cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)

        # applying Cosine Rule to find angle for all defects (between fingers)
        # with angle > 90 degrees and ignore defects
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]

            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])

            # find length of all sides of triangle
            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

            # apply cosine rule here
            angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

            # ignore angles > 90 and highlight rest with red dots
            if angle <= 90:
                count_defects += 1
                cv2.circle(crop_img, far, 1, [0, 0, 255], -1)
            dist = cv2.pointPolygonTest(cnt, far, True)

            # draw a line from start to end i.e. the convex points (finger tips)
            # (can skip this part)
            cv2.line(crop_img, start, end, [0, 255, 0], 2)
            cv2.circle(crop_img, far, 5, [0, 0, 255], -1)
            
        maxbid=models.Auction.objects.filter(ProductID=self.p_id).aggregate(Max('ClientInitialBid'))["ClientInitialBid__max"]
        userbid=models.Auction.objects.get(ProductID=self.p_id,ClientUsername=self.uname)
        global count
        # define actions required
        if count_defects == 1:
            cv2.putText(img, "2 Fingers", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            count=2
        elif count_defects == 2:
            cv2.putText(img, "3 Fingers", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            count=3
        elif count_defects == 3:
            cv2.putText(img, "4 Fingers", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            count=4
        elif count_defects == 4:
            cv2.putText(img, "5 Fingers", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            count=5
        else:
            cv2.putText(img, "0 Fingers", (50, 50), \
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            if count!=0:
                    userbid.ClientInitialBid=maxbid+(maxbid*5*count)/100
                    count=0
                    userbid.save()    

        # show appropriate images in windows

        self.fps.update()
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()

def endAuction(request,p_id):
    global b
    b=False
    global a
    del a
    mx=models.Auction.objects.filter(ProductID=p_id).aggregate(Max('ClientInitialBid'))["ClientInitialBid__max"]
    u=models.Auction.objects.filter(ProductID=p_id,ClientInitialBid=mx)
    print(u) 
    return render(request, 'Home/About_Us.html')

