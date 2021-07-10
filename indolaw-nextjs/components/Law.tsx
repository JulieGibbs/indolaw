import { useMemo } from "react";
import { Complex, Primitive, renderChildren, Structure, NodeMap, Metadata } from "utils/grammar";
import { fonts } from "utils/theme";
import { LawContext, getPenjelasanMapKey } from "utils/context-provider";
import Tooltip from "./Tooltip";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function Law(props: { law: Complex, metadata: Metadata, colorScheme: any }): JSX.Element {
  // This method requires a brute force traversal of PENJELASAN_PASAL_DEMI_PASAL
  // so we want to run it once & memoize
  const penjelasanMap = useMemo(() => extractPenjelasanMap(props.law), [props.law]);

  return (
    <LawContext.Provider value={{ penjelasanMap }}>
      <div>
        <style jsx>{`
        div {
          font-family: ${fonts.serif};
          font-size: 18px;
          color: ${props.colorScheme.text};
        }
      `}</style>
        {renderChildren(props.law)}
      </div>
      <Tooltip metadata={props.metadata}></Tooltip>
    </LawContext.Provider>
  );
}

function extractPenjelasanMap(law: Complex): NodeMap {
  const penjelasan = (law.children[law.children.length - 1] as Complex);
  const penjelasanPasalDemiPasal = penjelasan.children[penjelasan.children.length - 1];
  const penjelasanMap: NodeMap = {};

  function traverse(structure: Complex | Primitive) {
    if ("children" in structure && structure.children !== undefined) {
      structure = structure as Complex;
      if (structure.type === Structure.PENJELASAN_PASAL) {
        const pasalNumber = structure.children[0] as Primitive;
        const key = getPenjelasanMapKey(Structure.PASAL, pasalNumber.text);
        penjelasanMap[key] = structure;
      }

      for (let child of structure.children) {
        traverse(child);
      }
    }
  }

  traverse(penjelasanPasalDemiPasal);
  return penjelasanMap;
}
