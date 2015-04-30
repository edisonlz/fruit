package com.youku.api.gamestatis.old;

import java.util.ArrayList;
import java.util.HashMap;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.ScrollView;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;
import com.jjoe64.graphview.GraphView;
import com.special.ResideMenu.ResideMenu;
import com.youku.api.gamestatis.LoginActivity;
import com.youku.api.gamestatis.R;
import com.youku.api.gamestatis.R.id;
import com.youku.api.gamestatis.R.layout;
import com.youku.api.gamestatis.adapter.HomeIndexAdapter;
import com.youku.api.gamestatis.model.SummaryStatsModel;
import com.youku.api.gamestatis.model.HttpCallBackHandler;
import com.youku.api.gamestatis.model.LoginModel;
import com.youku.api.gamestatis.util.NetWorkUtil;
import com.youku.api.gamestatis.util.UnitFormat;

//import de.keyboardsurfer.android.widget.crouton.Crouton;

public class HomeFragment extends Fragment {

	private View parentView;
	private ResideMenu resideMenu;
	private MenuActivity parentActivity;
	protected ProgressBar mProgressBar;

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		parentView = inflater.inflate(R.layout.home, container, false);
		parentActivity = (MenuActivity) getActivity();
		setUpViews();

		SummaryStatsModel commonStats = new SummaryStatsModel(parentActivity);
		commonStats.get(new HttpCallBackHandler() {
			
			@Override
			public void onSuccess(HashMap<String, Object> result) {
				onHttpResponseCallback(result);
				mProgressBar.setVisibility(View.INVISIBLE);
			}
			
			@Override
			public void onFailure(Throwable error, String content){
				mProgressBar.setVisibility(View.INVISIBLE);
				if(error!=null) {
					Toast.makeText(parentActivity, error.getMessage()  ,Toast.LENGTH_SHORT).show();
        		}
				if(content!=null){
					Toast.makeText(parentActivity, content.toString() ,Toast.LENGTH_SHORT).show();
				}
			}
			
			@Override
			public void onFailure(Throwable error, JSONObject obj){
				mProgressBar.setVisibility(View.INVISIBLE);				
				if(error!=null) {
					Toast.makeText(parentActivity, error.getMessage()  ,Toast.LENGTH_SHORT).show();
        		}
				if(obj!=null){
					Toast.makeText(parentActivity, obj.toString() ,Toast.LENGTH_SHORT).show();
				}
				
				if(obj!=null){
					Integer error_code;
					try {
						error_code = obj.getInt("error_code");
						if(error_code==LoginModel.ErrorCodeNotLogin){
							Intent intent = new Intent(parentActivity, LoginActivity.class);
							parentActivity.startActivity(intent);
							parentActivity.finish();
						}
					} catch (JSONException e) {
						e.printStackTrace();
					}
				}
			}
			
		});
		return parentView;
	}

	private void setUpViews() {
		resideMenu = parentActivity.getResideMenu();
		mProgressBar = (ProgressBar) parentView.findViewById(R.id.ajax_loading);
		mProgressBar.setVisibility(View.VISIBLE);

		 
		ListView dataListView = (ListView) parentView.findViewById(R.id.dataListView);
		dataListView.addHeaderView(LayoutInflater.from(this.getActivity()).inflate(R.layout.home_table_header, null), null, false);
		
		
		// ignore gensture
		//ScrollView scrollhome = (ScrollView) parentView.findViewById(R.id.scrollHomeView);
		//resideMenu.addIgnoredView(scrollhome);
	}

	public void onHttpResponseCallback(HashMap<String, Object> result) {

		/*Set List View*/
		ListView listView = (ListView)parentView.findViewById(R.id.dataListView);
		HomeIndexAdapter adapter = new HomeIndexAdapter(parentActivity , (ArrayList<HashMap<String,Object>>)result.get("data"));
		listView.setAdapter(adapter);
		
		EditText dateText = (EditText)parentView.findViewById(R.id.dateText);
		dateText.setText(String.valueOf(result.get("date")));
		
		
		listView.setOnItemClickListener(new OnItemClickListener(){
			@Override
			public void onItemClick(AdapterView<?> parent, View view,
					int position, long id) {
				
				
				HashMap<String,Object> data = (HashMap<String, Object>) parent.getItemAtPosition(position);
				String item_id = String.valueOf(data.get("id"));
				MenuActivity act = (MenuActivity)parent.getContext();
				act.setProduct(item_id);
				BaseStatisFragment sf = new BaseStatisFragment();
				Bundle bundle = new Bundle();  
				bundle.putString("item_id", item_id);  
				sf.setArguments(bundle);  
				parentActivity.changeFragment(sf);
			}
		});
		

	}

	

}