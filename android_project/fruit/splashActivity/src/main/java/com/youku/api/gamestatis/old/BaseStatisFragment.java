package com.youku.api.gamestatis.old;

import java.util.ArrayList;
import java.util.HashMap;

import org.json.JSONException;
import org.json.JSONObject;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.helper.StaticLabelsFormatter;
import com.jjoe64.graphview.series.BarGraphSeries;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;
import com.special.ResideMenu.ResideMenu;
import com.youku.api.gamestatis.LoginActivity;
import com.youku.api.gamestatis.R;
import com.youku.api.gamestatis.R.id;
import com.youku.api.gamestatis.R.layout;
import com.youku.api.gamestatis.adapter.HomeIndexAdapter;
import com.youku.api.gamestatis.model.BaseStatisModel;
import com.youku.api.gamestatis.model.HttpCallBackHandler;
import com.youku.api.gamestatis.model.LoginModel;
import com.youku.api.gamestatis.model.SummaryStatsModel;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewGroup.LayoutParams;
import android.widget.AdapterView;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.AdapterView.OnItemClickListener;

public class BaseStatisFragment extends Fragment {

	private View parentView;
	private MenuActivity parentActivity;
	protected ProgressBar mProgressBar;
	private ResideMenu resideMenu;

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {

		parentView = inflater.inflate(R.layout.basestatis, container, false);
		parentActivity = (MenuActivity) getActivity();
		
		this.setUpViews();

		String item_id = parentActivity.getProduct();
		if (item_id == null) {
			Toast.makeText(parentActivity, String.valueOf("请选择产品线!"),
					Toast.LENGTH_SHORT).show();
			return parentView;
		}



//		BaseStatisModel commonStats = new BaseStatisModel(parentActivity);
//		commonStats.get("2",new HttpCallBackHandler() {
//
//			@Override
//			public void onSuccess(HashMap<String, Object> result) {
//				onHttpResponseCallback(result);
//				mProgressBar.setVisibility(View.INVISIBLE);
//			}
//
//			@Override
//			public void onFailure(Throwable error, String content) {
//				mProgressBar.setVisibility(View.INVISIBLE);
//				if (error != null) {
//					Toast.makeText(parentActivity, error.getMessage(),
//							Toast.LENGTH_SHORT).show();
//				}
//				if (content != null) {
//					Toast.makeText(parentActivity, content.toString(),
//							Toast.LENGTH_SHORT).show();
//				}
//			}
//
//			@Override
//			public void onFailure(Throwable error, JSONObject obj) {
//				mProgressBar.setVisibility(View.INVISIBLE);
//				if (error != null) {
//					Toast.makeText(parentActivity, error.getMessage(),
//							Toast.LENGTH_SHORT).show();
//				}
//				if (obj != null) {
//					Toast.makeText(parentActivity, obj.toString(),
//							Toast.LENGTH_SHORT).show();
//				}
//
//				if (obj != null) {
//					Integer error_code;
//					try {
//						error_code = obj.getInt("error_code");
//						if (error_code == LoginModel.ErrorCodeNotLogin) {
//							Intent intent = new Intent(parentActivity,
//									LoginActivity.class);
//							parentActivity.startActivity(intent);
//							parentActivity.finish();
//						}
//					} catch (JSONException e) {
//						e.printStackTrace();
//					}
//				}
//			}
//
//		});

		return parentView;
	}
	
	private void setUpViews() {
		resideMenu = parentActivity.getResideMenu();
		mProgressBar = (ProgressBar) parentView.findViewById(R.id.ajax_loading);
		mProgressBar.setVisibility(View.VISIBLE);
	}

	public void onHttpResponseCallback(HashMap<String, Object> result) {

		/* Set List View */
		
		HashMap<String,Object> data = (HashMap<String,Object>)result.get("data");
		EditText startdateText =  (EditText)parentView.findViewById(R.id.startdateText);
		EditText enddateText =   (EditText)parentView.findViewById(R.id.enddateText);
		TextView productText = (TextView)parentView.findViewById(R.id.productText);
		
		startdateText.setText(String.valueOf(result.get("startdate")));
		enddateText.setText(String.valueOf(result.get("enddate")));
		productText.setText(String.valueOf(result.get("product_name")));
		
		GraphView graphLayout_uv = (GraphView) parentView.findViewById(R.id.graphViewUV);
		HashMap<String,Object> uv_line = (HashMap<String,Object>) data.get("uv_line");
		graphLayout_uv.removeAllSeries();
		drawGraphView(graphLayout_uv , uv_line , Color.rgb(0,204,204));
		
		
		GraphView graphLayout_vv = (GraphView) parentView.findViewById(R.id.graphViewVV);
		graphLayout_vv.removeAllSeries();
		
		HashMap<String,Object> vv_line = (HashMap<String,Object>) data.get("vv_line");
		drawGraphView(graphLayout_vv , vv_line , Color.rgb(245,63,63));
	}

	private void drawGraphView(GraphView graphView,
			HashMap<String, Object> uv_line,int color) {

		ArrayList<Integer> x = (ArrayList<Integer>) uv_line.get("x");
		ArrayList<Integer> y = (ArrayList<Integer>) uv_line.get("y");

		int num = x.size();

		if (num <= 0) {
			return;
		}

		Integer[] dates = new Integer[num];
		DataPoint[] data = new DataPoint[num];

		int x_max = 0;
		int y_max = 0;
		for (int i = 0; i < num; i++) {
			dates[i] = x.get(i);
			data[i] = new DataPoint(i, y.get(i));
			x_max = i;
		}
		
		Log.e("data", y.toString());

		BarGraphSeries<DataPoint> seriesYouku = new BarGraphSeries<DataPoint>(
				data);
		seriesYouku.setColor(color);
		graphView.addSeries(seriesYouku);
		
		//graphView.setLegendRenderer(mLegendRenderer);

//		LinearLayout.LayoutParams graphViewpParams = new LinearLayout.LayoutParams(
//				LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT);
		
		//graphView.setLayoutParams(graphViewpParams);

		graphView.getViewport().setXAxisBoundsManual(true);
		graphView.getViewport().setMinX(0);
		graphView.getViewport().setMaxX(x_max);

		graphView.getGridLabelRenderer().setGridColor(Color.CYAN);
		graphView.getGridLabelRenderer().setPadding(4);

		/* set x label */
		 Integer istep = dates.length / 2;
		 String[] x_lables = new String[]{dates[0].toString(),
		 dates[istep].toString(),
		 dates[dates.length-1].toString()};
	
		 
		 StaticLabelsFormatter staticLabelsFormatter = new StaticLabelsFormatter(graphView);
		 staticLabelsFormatter.setHorizontalLabels(x_lables);
		 graphView.getGridLabelRenderer().setLabelFormatter(staticLabelsFormatter);
		 
		 //graphView.getGridLabelRenderer().setH(x_lables);
		// graphView.setCustomLabelFormatter(new CustomLabelFormatter() {
		// @Override
		// public String formatLabel(double value, boolean isValueX) {
		// return UnitFormat.toTenThousand(value);
		// }
		// });
	}
}
