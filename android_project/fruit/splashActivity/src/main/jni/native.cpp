#include <jni.h>
#include <string.h>
#include <android/log.h>
#include <unistd.h>  


extern "C"  
JNIEXPORT jstring JNICALL Java_com_youku_api_gamestatis_model_BaseModel_helloGay(JNIEnv *env, jobject obj,jstring jstr)
{

    
   char* rtn = NULL;    
   jclass clsstring = env->FindClass("java/lang/String");    
   jstring strencode = env->NewStringUTF("utf-8");    
   jmethodID mid = env->GetMethodID(clsstring, "getBytes", "(Ljava/lang/String;)[B");    
   jbyteArray barr= (jbyteArray)env->CallObjectMethod(jstr, mid, strencode);    
   jsize alen = env->GetArrayLength(barr);    
   jbyte* ba = env->GetByteArrayElements(barr, JNI_FALSE);    
   if (alen > 0)    
   {    
     rtn = (char*)malloc(alen + 1);    
     memcpy(rtn, ba, alen);    
     rtn[alen] = 0;    
   }
   env->ReleaseByteArrayElements(barr, ba, 0);    


    int l = 16;
    char buf[l+1];

    const char *classname = "com/youku/api/gamestatis/model/BaseModel";  
 
    jclass dpclazz = (*env).FindClass(classname);  
    
    if(dpclazz == NULL){
        return  (*env).NewStringUTF("adamcaewqadc");
    }


    jlong a = 1+2;
    int i =0;
    
    while(i<l){
        if(i%2==0){
            buf[i] = '0'+i; 
        }else if(i%3==0){
            buf[i]= 'A'+i+1;            
        }
        else{
            buf[i]= 'a'+i+3;        
        }
        i++;
    }
    buf[16]= '\0';
    
    jlong t = 3+4;

    jlong c = a + t;

    
    int j=0;
    char at[32+1];
    while(j<8){
        at[j] = buf[j];
        j++;
    }
    at[32] = '\0';

    while(j<32){
        at[j] = rtn[j];
        j++;
    }

    jstring n = (*env).NewStringUTF(at);

    return n;

}

extern "C"  
JNIEXPORT jstring JNICALL Java_com_youku_api_gamestatis_model_BaseModel_toJi(JNIEnv *env, jclass jcl,  
        jobject context_object) {  
    jclass context_class = env->GetObjectClass(context_object);  
  
        //context.getPackageManager()  
        jmethodID methodId = env->GetMethodID(context_class, "getPackageManager", "()Landroid/content/pm/PackageManager;");  
        jobject package_manager_object = env->CallObjectMethod(context_object, methodId);  
        if (package_manager_object == NULL) {  
            __android_log_print(ANDROID_LOG_INFO, "JNITag","getPackageManager() Failed!");  
            return NULL;  
        }  
  
        //context.getPackageName()  
        methodId = env->GetMethodID(context_class, "getPackageName", "()Ljava/lang/String;");  
        jstring package_name_string = (jstring)env->CallObjectMethod(context_object, methodId);  
        if (package_name_string == NULL) {  
            __android_log_print(ANDROID_LOG_INFO, "JNITag","getPackageName() Failed!");  
            return NULL;  
        }  
  
        env->DeleteLocalRef(context_class);  
  
        //PackageManager.getPackageInfo(Sting, int)  
        jclass pack_manager_class = env->GetObjectClass(package_manager_object);  
        methodId = env->GetMethodID(pack_manager_class, "getPackageInfo", "(Ljava/lang/String;I)Landroid/content/pm/PackageInfo;");  
        env->DeleteLocalRef(pack_manager_class);  
        jobject package_info_object = env->CallObjectMethod(package_manager_object, methodId, package_name_string, 64);  
        if (package_info_object == NULL) {  
            __android_log_print(ANDROID_LOG_INFO, "JNITag","getPackageInfo() Failed!");  
            return NULL;  
        }  
  
        env->DeleteLocalRef(package_manager_object);  
  
        //PackageInfo.signatures[0]  
        jclass package_info_class = env->GetObjectClass(package_info_object);  
        jfieldID fieldId = env->GetFieldID(package_info_class, "signatures", "[Landroid/content/pm/Signature;");  
        env->DeleteLocalRef(package_info_class);  
        jobjectArray signature_object_array = (jobjectArray)env->GetObjectField(package_info_object, fieldId);  
        if (signature_object_array == NULL) {  
            __android_log_print(ANDROID_LOG_INFO, "JNITag","PackageInfo.signatures[] is null");  
            return NULL;  
        }  
        jobject signature_object = env->GetObjectArrayElement(signature_object_array, 0);  
  
        env->DeleteLocalRef(package_info_object);  
  
        //Signature.toCharsString()  
        jclass signature_class = env->GetObjectClass(signature_object);  
        methodId = env->GetMethodID(signature_class, "toCharsString", "()Ljava/lang/String;");  
        env->DeleteLocalRef(signature_class);  
        jstring signature_string = (jstring) env->CallObjectMethod(signature_object, methodId);  

        // cls = (*env)->GetObjectClass(env, signature_object);
        // mid = (*env)->GetMethodID(env, cls, "hashCode", "()I");
        // int sig_value = (int)(*env)->CallIntMethod(env, signature_object, mid);
        // return sig_value;
  
        return signature_string;  
}  