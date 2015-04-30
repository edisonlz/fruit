package com.youku.api.gamestatis;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;

import org.json.JSONException;
import org.json.JSONObject;


import android.app.DatePickerDialog;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.Window;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.youku.api.gamestatis.adapter.HomeIndexAdapter;
import com.youku.api.gamestatis.adapter.ShowRankAdapter;
import com.youku.api.gamestatis.base.BaseActivity;
import com.youku.api.gamestatis.model.BaseStatisModel;
import com.youku.api.gamestatis.model.HttpCallBackHandler;
import com.youku.api.gamestatis.model.LoginModel;
import com.youku.api.gamestatis.model.ShowRankModel;

import de.keyboardsurfer.android.widget.crouton.Crouton;
import de.keyboardsurfer.android.widget.crouton.Style;

public class ShowRankActivity extends BaseActivity  {

	protected ProgressBar mProgressBar;
	private Context mContext;
	private Spinner platformSpinner;
	private Spinner deivceSpinner;
	private Spinner channleShowSpinner;
    private ArrayAdapter<String> platformAdapter;
    private ArrayAdapter<String> diviceAdapter;
    private Button  doButton; 
    private EditText dateText;
    private ListView datalistView;
    private Boolean changeDate = false;
    Calendar myCalendar = Calendar.getInstance();

    
    private DatePickerDialog.OnDateSetListener datePickerListener 
	    = new DatePickerDialog.OnDateSetListener() {
		public void onDateSet(DatePicker view, int selectedYear,
		int selectedMonth, int selectedDay) {
		dateText.setText(String.format("%d%02d%02d", selectedYear,selectedMonth+1,selectedDay));
		}
		
	};
	
	public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.requestWindowFeature(Window.FEATURE_NO_TITLE);
        
        mContext = this;
        
        setContentView(R.layout.showrank);
        
        setUpViews();
        
        String item_id = this.getProduct();
		if (item_id == null) {
			Toast.makeText(this, String.valueOf("请选择产品线!"),
					Toast.LENGTH_SHORT).show();
			return;
		}

		loadData();
	}
	
	private void setUpViews() {
		
		
		mProgressBar = (ProgressBar) this.findViewById(R.id.ajax_showrank_loading);
		mProgressBar.setVisibility(View.VISIBLE);
		
		platformSpinner = (Spinner) findViewById(R.id.platformShowRankSpinner);
        
        deivceSpinner = (Spinner) findViewById(R.id.deivceShowRankSpinner);
        
        channleShowSpinner = (Spinner) findViewById(R.id.channleShowSpinner);
        
        doButton = (Button)findViewById(R.id.doShowRankButton);
        
        datalistView = (ListView)findViewById(R.id.dataRanklistView);
        
        datalistView.addHeaderView(LayoutInflater.from(this).inflate(R.layout.showrank_itemheader, null), null, false);
        
        doButton.setOnClickListener(new View.OnClickListener(){

			@Override
			public void onClick(View v) {
				loadData();
			}});
        
        dateText = (EditText) findViewById(R.id.dateShowRankText);
        
        dateText.setFocusable(false);
        
        dateText.setOnClickListener(new View.OnClickListener() {
 
			@Override
			public void onClick(View v) {

				Editable date = dateText.getText();
				
				int year = Integer.valueOf(date.toString().substring(0,4));
				int month = Integer.valueOf(date.toString().substring(4,6))-1;
				int day = Integer.valueOf(date.toString().substring(6,8));
				changeDate = true;
				new DatePickerDialog(ShowRankActivity.this, datePickerListener, year,month,day).show();
			}
 
		});
        
	}

	
	private void loadData(){
		mProgressBar.setVisibility(View.VISIBLE);	
		
		String splatform = platformSpinner.getSelectedItem().toString();
		String sdevice = deivceSpinner.getSelectedItem().toString();
		String schannel = channleShowSpinner.getSelectedItem().toString();
		
		String date = null;
		
		if(changeDate){
			date = dateText.getText().toString();
		}
		
		int device = this.deivceMap.get(sdevice);
		int platform = this.platformMap.get(splatform);;
        
		
		ShowRankModel showRank = new ShowRankModel(this);
		showRank.get(this.getProduct(),platform,device,schannel,date,new HttpCallBackHandler() {

			@Override
			public void onSuccess(HashMap<String, Object> result) {
				onHttpResponseCallback(result);
				mProgressBar.setVisibility(View.INVISIBLE);
			}

			@Override
			public void onFailure(Throwable error, String content) {
				mProgressBar.setVisibility(View.INVISIBLE);
				if (error != null) {
					Crouton.makeText(ShowRankActivity.this,   error.getMessage(), Style.CONFIRM).show();
				}
				if (content != null) {
					Crouton.makeText(ShowRankActivity.this, content.toString(), Style.CONFIRM).show();
				}
			}

			@Override
			public void onFailure(Throwable error, JSONObject obj) {
				mProgressBar.setVisibility(View.INVISIBLE);
				if (error != null) {
					String msg = error.getMessage();
					if(msg==null){
						msg = "读取接口错误";
					}
					Crouton.makeText(ShowRankActivity.this,   msg, Style.CONFIRM).show();
				}
				if (obj != null) {
					Crouton.makeText(ShowRankActivity.this, obj.toString(), Style.CONFIRM).show();
				}
			}

		});
	}

	public void onHttpResponseCallback(HashMap<String, Object> result) {
		TextView product  = (TextView)findViewById( R.id.productShowRankText);
		
		//dateText.setText(text);
		
		ArrayList<HashMap<String,Object>> data =(ArrayList<HashMap<String,Object>>)result.get("data");
		
		if(data==null){
			Crouton.makeText(ShowRankActivity.this,  "请求结果为空!", Style.CONFIRM).show();
		}
		
		ShowRankAdapter adapter = new ShowRankAdapter(this , data);
		datalistView.setAdapter(adapter);
	}
}