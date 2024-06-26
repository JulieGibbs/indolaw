import { CSSProperties, useState } from "react";
import { Complex, Primitive, renderStructure } from "utils/grammar";
import { useAppContext } from "../utils/context-provider";
import PrimitiveStructure from "./PrimitiveStructure";
import ReactDOMServer from "react-dom/server";
import * as clipboard from "clipboard-polyfill";
import CopyButton from "./CopyButton";
import { renderCopyHtml } from "utils/copypaste";
import { useIsMobile } from "utils/hooks";

export default function PenjelasanPasal(props: {
  structure: Complex;
  numOfHeadingLines: number;
  collapseOnDefault?: boolean;
}): JSX.Element {
  const { structure, numOfHeadingLines, collapseOnDefault } = props;
  // content is visible on default if it's not collapsible, otherwise, collapse content on first view
  const [isContentVisible, setIsContentVisible] = useState(!collapseOnDefault);
  const [isHoverOnCopyButton, setIsHoverOnCopyButton] = useState(false);
  const { colorScheme } = useAppContext();
  const isMobile = useIsMobile();

  const headingStyle: CSSProperties = {
    marginLeft: "0px",
    textAlign: "center",
    margin: "8px 0",
    fontWeight: 700,
  };

  const copyButton = (
    <CopyButton
      onClick={async () => {
        const item = new clipboard.ClipboardItem({
          "text/html": new Blob(
            [
              ReactDOMServer.renderToStaticMarkup(
                renderCopyHtml(structure)
              )
            ],
            { type: "text/html" }
          ),
        });
        await clipboard.write([item]);
      }}
      onMouseEnter={() => setIsHoverOnCopyButton(true)}
      onMouseLeave={() => setIsHoverOnCopyButton(false)}
    />
  );

  return (
    <>
      <style jsx>{`
        .group {
          margin: 20px auto;
          background-color: ${colorScheme.subcontent.background};
          padding: 10px 0;
          border-radius: 8px;
          border: 1px solid ${colorScheme.clickable};
        }

        .title:hover {
          cursor: pointer;
        }

        .title {
          margin: 8px 0;
          font-weight: 700;
          line-height: 1.5;
          display: flex;
          justify-content: center;
          text-transform: capitalize;
        }

        .content {
          margin: 20px;
          padding: 4px ${isMobile ? '0' : '20px'};
          background-color: ${isHoverOnCopyButton ? colorScheme.clickableBackground : 'none'};
          border-radius: 8px;
        }

        .heading-container {
          display: flex;
          justify-content: center;
        }

        .material-icons.style {
          vertical-align: bottom;
          padding-top: 2px;
          color: ${colorScheme.clickable};
        }
      `}</style>
      <div className="group">
        {collapseOnDefault && (
          <div
            className="title"
            onClick={() => setIsContentVisible(!isContentVisible)}
          >
            {structure.type.toString().toLowerCase().replace(/_/g, " ")}
            <i className="material-icons style">
              {isContentVisible ? "expand_less" : "expand_more"}
            </i>
          </div>
        )}

        {isContentVisible && (
          <div className="content">
            <div id={structure.id} className="heading-container">
              <PrimitiveStructure
                structure={structure.children[0] as Primitive}
                customStyle={headingStyle}
              />
              {!isMobile && copyButton}
            </div>

            {structure.children.slice(numOfHeadingLines).map((child, idx) => {
              child = child as Primitive;
              // The if-statement below should be temporary, as the current parser parses "TAMBAHAN xxxx" as part of penjelasan
              // which should not be the intended behavior
              if (
                child.text &&
                child.text.startsWith(
                  "TAMBAHAN LEMBARAN NEGARA REPUBLIK INDONESIA"
                )
              ) {
                return <></>;
              }

              return renderStructure(child, idx, isMobile);
            })}
          </div>
        )}
      </div>
    </>
  );
}
