
package com.youku.api.gamestatis.listviewitem;

import java.text.DecimalFormat;

import android.R.color;
import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.view.LayoutInflater;
import android.view.View;

import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.components.Legend;
import com.github.mikephil.charting.components.Legend.LegendForm;
import com.github.mikephil.charting.components.Legend.LegendPosition;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.XAxis.XAxisPosition;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.data.ChartData;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.utils.ValueFormatter;
import com.youku.api.gamestatis.R;

public class LineChartItem extends ChartItem {

    private Typeface mTf;
    private  MyValueFormatter formater;
    private int yMax;
    private int yMin;
    private boolean is_viewport = true;
    
    public LineChartItem(ChartData<?> cd, Context c,int divide,String suffix,int yMax,int yMin,boolean is_viewport){
    	super(cd);
    	this.formater = new MyValueFormatter(divide,suffix);
    	this.yMax = yMax + (int)(yMax*0.1);
    	this.yMin = yMin -(int)(yMin * 0.1);
    	this.is_viewport = is_viewport;
    }
    
    
    private static class MyValueFormatter implements ValueFormatter {

        private String suffix;
        private int divide;

        public MyValueFormatter(int divide,String suffix) {
            this.divide = divide;
            this.suffix =suffix;
        }

        @Override
        public String getFormattedValue(float value) {
        	return String.format("%s%s",(int)value/divide,suffix);
        }
    }

    @Override
    public int getItemType() {
        return TYPE_LINECHART;
    }

    @Override
    public View getView(int position, View convertView, Context c) {

        ViewHolder holder = null;

        if (convertView == null) {

            holder = new ViewHolder();

            convertView = LayoutInflater.from(c).inflate(
                    R.layout.list_item_linechart, null);
            holder.chart = (LineChart) convertView.findViewById(R.id.chart);

            convertView.setTag(holder);

        } else {
            holder = (ViewHolder) convertView.getTag();
        }

        // apply styling
        // holder.chart.setValueTypeface(mTf);
        holder.chart.setDescription("");
        holder.chart.setDrawGridBackground(false);
        holder.chart.setTouchEnabled(true);
        holder.chart.setBackgroundColor(Color.WHITE);
        

        XAxis xAxis = holder.chart.getXAxis();
        xAxis.setPosition(XAxisPosition.BOTTOM);
        xAxis.setDrawGridLines(false);
        xAxis.setDrawAxisLine(true);
        //xAxis.setGridColor(Color.WHITE);
        //xAxis.setTextColor(Color.WHITE);

        YAxis leftAxis = holder.chart.getAxisLeft();
        leftAxis.setLabelCount(5);
        leftAxis.setValueFormatter(this.formater);
        if(is_viewport){
        	leftAxis.setStartAtZero(false);
        	leftAxis.setAxisMaxValue(yMax);
        	leftAxis.setAxisMinValue(yMin);
        }
        //leftAxis.setTextColor(Color.WHITE);
        
        YAxis rightAxis = holder.chart.getAxisRight();
        rightAxis.setLabelCount(5);
        rightAxis.setDrawGridLines(false);
        rightAxis.setValueFormatter(this.formater);
        rightAxis.setEnabled(false);
        //rightAxis.setTextColor(Color.WHITE);

        // set data
        holder.chart.setData((LineData) mChartData);
        
        Legend l = holder.chart.getLegend();
        l.setFormSize(10f); // set the size of the legend forms/shapes
        l.setForm(LegendForm.CIRCLE); // set what type of form/shape should be used
        l.setPosition(LegendPosition.BELOW_CHART_LEFT);
        l.setTextSize(12f);
        //l.setTextColor(Color.WHITE);

        // do not forget to refresh the chart
        holder.chart.invalidate();
        //holder.chart.animateX(500);

        return convertView;
    }

    private static class ViewHolder {
        LineChart chart;
    }
}
