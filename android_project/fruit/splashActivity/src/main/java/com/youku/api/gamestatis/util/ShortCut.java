package com.youku.api.gamestatis.util;


import java.util.List;

import android.content.ContentResolver;
import android.content.Context;
import android.content.Intent;
import android.content.Intent.ShortcutIconResource;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.ProviderInfo;
import android.database.Cursor;
import android.net.Uri;

public class ShortCut {

	public static boolean hasShortcut(Context context , int app_name)
	{
		boolean isInstallShortcut = false;
		final ContentResolver cr = context.getContentResolver();
		final String AUTHORITY = ShortCut.getAuthorityFromPermission(context , "com.android.launcher.settings");
		final Uri CONTENT_URI = Uri.parse("content://" +AUTHORITY + "/favorites?notify=true");
		Cursor c = cr.query(CONTENT_URI,new String[] {"title","iconResource" },"title=?",
		new String[] {context.getString(app_name).trim()}, null);
		if( c != null && c.getCount() > 0){
			isInstallShortcut = true;
		}
		return isInstallShortcut;
	}
	
	
	public static void createShortcut(Context context , int app_name,int icon){
		
			Intent shortcut = new Intent("com.android.launcher.action.INSTALL_SHORTCUT");

			//快捷方式的名称
			shortcut.putExtra(Intent.EXTRA_SHORTCUT_NAME, context.getString(app_name)); 
			shortcut.putExtra("duplicate", false); //不允许重复创建  
	
			Intent shortcutIntent = new Intent(Intent.ACTION_MAIN);
			shortcutIntent.setClassName(context, context.getClass().getName());
			shortcut.putExtra(Intent.EXTRA_SHORTCUT_INTENT, shortcutIntent);
			
			ShortcutIconResource iconRes = Intent.ShortcutIconResource.fromContext(context, icon); 
			shortcut.putExtra(Intent.EXTRA_SHORTCUT_ICON_RESOURCE, iconRes);

			context.sendBroadcast(shortcut);
	}
	
	protected static String getAuthorityFromPermission(Context context, String permission){
		
	    if (permission == null) return null;
	    List<PackageInfo> packs = context.getPackageManager().getInstalledPackages(PackageManager.GET_PROVIDERS);
	    if (packs != null) {
	        for (PackageInfo pack : packs) { 
	            ProviderInfo[] providers = pack.providers; 
	            if (providers != null) { 
	                for (ProviderInfo provider : providers) { 
	                    if (permission.equals(provider.readPermission)) return provider.authority;
	                    if (permission.equals(provider.writePermission)) return provider.authority;
	                } 
	            }
	        }
	    }
	    return null;
	}
}
