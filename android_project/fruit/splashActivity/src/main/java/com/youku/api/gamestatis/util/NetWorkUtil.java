package com.youku.api.gamestatis.util;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ComponentName;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.net.ConnectivityManager;

public class NetWorkUtil {
	
	/**
	 * ����������״̬�����ж�
	 * @return  true, ���ã� false�� ������
	 */
	public static boolean isOpenNetwork(Context context) {
		ConnectivityManager connManager = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
		if(connManager.getActiveNetworkInfo() != null) {
			return connManager.getActiveNetworkInfo().isAvailable();
		}
		return false;
	}
	
	
	public static boolean CheckNetworkState(final Activity context)
    {
		if(NetWorkUtil.isOpenNetwork(context)){
			return true;
		}
		
        AlertDialog.Builder builder = new AlertDialog.Builder(context);
        builder.setIcon(android.R.drawable.ic_dialog_alert);
        builder.setTitle("NetWorkSettings̬");
        builder.setMessage("No Network connect to mobile internet,Set now?");
        builder.setPositiveButton("Settings", new DialogInterface.OnClickListener() {
            
            @Override
            public void onClick(DialogInterface dialog, int which) {
            	
        		if(android.os.Build.VERSION.SDK_INT > 10 ){
        			context.startActivity(new Intent(android.provider.Settings.ACTION_SETTINGS));
        		}else {
        			context.startActivity(new Intent(android.provider.Settings.ACTION_WIRELESS_SETTINGS));
        		}
            }
        });
        
        builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
            
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.cancel();
                context.finish();
            }
        });
        builder.create();
        builder.show();
        return false;
    }
 
	
}
