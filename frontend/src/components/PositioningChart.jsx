import {
  CartesianGrid,
  ReferenceLine,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
  ZAxis,
} from "recharts";

function ChartTooltip({ active, payload }) {
  if (!active || !payload?.length) return null;
  const item = payload[0].payload;

  return (
    <div className="chart-tooltip">
      <strong>{item.brand}</strong>
      <span>{item.product_id}</span>
      <dl>
        <div>
          <dt>가격</dt>
          <dd>{item.price.toLocaleString()}원</dd>
        </div>
        <div>
          <dt>총장</dt>
          <dd>{item.length}cm</dd>
        </div>
        <div>
          <dt>통</dt>
          <dd>{item.width}cm</dd>
        </div>
        <div>
          <dt>평점</dt>
          <dd>{item.rating}</dd>
        </div>
        <div>
          <dt>사분면</dt>
          <dd>{item.quadrant}</dd>
        </div>
      </dl>
    </div>
  );
}

export default function PositioningChart({ data }) {
  const products = data.products.filter((product) => product.product_id !== data.target_product_id);
  const target = data.products.filter((product) => product.product_id === data.target_product_id);
  const xValues = data.products.map((product) => product.length);
  const yValues = data.products.map((product) => product.width);
  const xMin = Math.floor(Math.min(...xValues) - 2);
  const xMax = Math.ceil(Math.max(...xValues) + 2);
  const yMin = Math.floor(Math.min(...yValues) - 2);
  const yMax = Math.ceil(Math.max(...yValues) + 2);

  return (
    <div className="chart-wrap">
      <div className="quadrant-label q1">Short & Wide</div>
      <div className="quadrant-label q2">Long & Wide</div>
      <div className="quadrant-label q3">Short & Slim</div>
      <div className="quadrant-label q4">Long & Slim</div>
      <ResponsiveContainer width="100%" height={520}>
        <ScatterChart margin={{ top: 24, right: 26, bottom: 36, left: 20 }}>
          <CartesianGrid stroke="#dce3e8" strokeDasharray="4 4" />
          <XAxis
            type="number"
            dataKey="length"
            name="총장"
            unit="cm"
            domain={[xMin, xMax]}
            tick={{ fill: "#58707c", fontSize: 12 }}
            label={{ value: "총장 length (cm)", position: "insideBottom", offset: -18, fill: "#49616d" }}
          />
          <YAxis
            type="number"
            dataKey="width"
            name="통"
            unit="cm"
            domain={[yMin, yMax]}
            tick={{ fill: "#58707c", fontSize: 12 }}
            label={{ value: "통 width (cm)", angle: -90, position: "insideLeft", fill: "#49616d" }}
          />
          <ZAxis type="number" range={[46, 120]} />
          <Tooltip cursor={{ strokeDasharray: "3 3" }} content={<ChartTooltip />} />
          <ReferenceLine x={data.length_split} stroke="#233842" strokeWidth={1.5} />
          <ReferenceLine y={data.width_split} stroke="#233842" strokeWidth={1.5} />
          <Scatter name="전체 상품" data={products} fill="#4d8fa3" fillOpacity={0.72} />
          <Scatter name="Product A" data={target} fill="#d44f3d" shape="star" />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}
