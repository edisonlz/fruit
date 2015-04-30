package com.youku.api.gamestatis.base;

import java.util.ArrayList;
import java.util.HashMap;

import com.android.intro.custorm.imageview.SampleApplication;
import com.youku.api.gamestatis.BaseStatisActivity;
import com.youku.api.gamestatis.HomeActivity;
import com.youku.api.gamestatis.LoginActivity;
import com.youku.api.gamestatis.R;
import com.youku.api.gamestatis.R.id;
import com.youku.api.gamestatis.R.layout;
import com.youku.api.gamestatis.ShowRankActivity;
import com.youku.api.gamestatis.model.LoginModel;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.ListFragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.AdapterView.OnItemClickListener;


public class MenuFragment  extends ListFragment {
	
	private SampleApplication app;

	private  String[][] Items = new String[][]{
			{"首页","1"},
			{"基础统计项","2"},
			{"剧集排行","3"}
	};
	
	
	private View view;
	
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		
		view = inflater.inflate(R.layout.list, null);
	   return view;
	}
	
	public String getUsername(){
    	Persistence ps = app.getPersistence();
		return ps.get("username");
    }

	public void onActivityCreated(Bundle savedInstanceState) {
		super.onActivityCreated(savedInstanceState);
		
		app = (SampleApplication) this.getActivity().getApplication();
		
		ArrayList<Integer> icons = new ArrayList<Integer>();
		icons.add(R.drawable.icon_home);
		icons.add(R.drawable.icon_calendar);
		icons.add(R.drawable.icon_calendar);
		
		SampleAdapter adapter = new SampleAdapter(getActivity());
		for (int i = 0; i < Items.length; i++) {
			adapter.add(new SampleItem(Items[i][0], icons.get(i)));
		}
		setListAdapter(adapter);
		
		TextView logout = (TextView)this.getActivity().findViewById(R.id.logout);
		
		TextView username = (TextView)this.getActivity().findViewById(R.id.username);
		username.setText(this.getUsername());
		
		logout.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				do_Logout();
			}
			
		});
		
		

	}

	private class SampleItem {
		public String tag;
		public int iconRes;
		public SampleItem(String tag, int iconRes) {
			this.tag = tag; 
			this.iconRes = iconRes;
		}
	}

	public class SampleAdapter extends ArrayAdapter<SampleItem> {

		public SampleAdapter(Context context) {
			super(context, 0);
		}

		public View getView(int position, View convertView, ViewGroup parent) {
			if (convertView == null) {
				convertView = LayoutInflater.from(getContext()).inflate(R.layout.row, null);
			}
			ImageView icon = (ImageView) convertView.findViewById(R.id.row_icon);
			icon.setImageResource(getItem(position).iconRes);
			TextView title = (TextView) convertView.findViewById(R.id.row_title);
			title.setText(getItem(position).tag);

			return convertView;
		}

	}
	
	@Override
	public void onListItemClick(ListView lv, View v, int position, long id) {
		
		String[] data =  Items[position];
		
		String type = data[1];
		Intent intent ;
		
		boolean finished = false;
		switch(Integer.valueOf(type)){
			
			case 1:
				intent = new Intent(this.getActivity(), HomeActivity.class);
				this.startActivity(intent);
				break;
			case 2:
				intent = new Intent(this.getActivity(), BaseStatisActivity.class);
				this.startActivity(intent);
				finished =true;
				break;
			case 3:
				intent = new Intent(this.getActivity(), ShowRankActivity.class);
				this.startActivity(intent);
				finished =true;
				break;
			default:
				intent = new Intent(this.getActivity(), HomeActivity.class);
				this.startActivity(intent);
				finished =true;
		}
		
		
		((BaseActivity)this.getActivity()).sm.showContent();
		this.startActivity(intent);
	}
	
	private void do_Logout(){
		Intent intent = new Intent(this.getActivity(), LoginActivity.class);
        this.startActivity(intent);
        LoginModel loginModel = new LoginModel(this.getActivity());
        loginModel.logout();
        this.getActivity().finish();
	}
}
